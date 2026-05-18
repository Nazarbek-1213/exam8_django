from django.contrib import messages as flash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from Bid.models import Bid
from .forms import ProjectForm
from .models import Project, SavedProject


@login_required(login_url='login')
def CreateProView(request):
    if request.user.role != 'client':
        return redirect('main_freelancer')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.status = 'open'
            project.save()
            flash.success(request, "Loyiha muvaffaqiyatli yaratildi!")
            return redirect('main_client')
    else:
        form = ProjectForm()

    return render(request, 'create_post.html', {'form': form})


@login_required(login_url='login')
def SelfProjectsView(request):
    projects = Project.objects.filter(client=request.user).order_by('-created_at')
    paginator = Paginator(projects, 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'myprojects.html', {'projects': page, 'page_obj': page})


@login_required(login_url='login')
def ProjectdetailsView(request, id):
    user = request.user
    project = get_object_or_404(Project, id=id)

    bids = Bid.objects.filter(project=project).select_related('freelancer')

    my_bid = None
    is_saved = False
    if user.role == 'freelancer':
        my_bid = Bid.objects.filter(project=project, freelancer=user).first()
        is_saved = SavedProject.objects.filter(user=user, project=project).exists()

    similar_projects = Project.objects.filter(
        category=project.category,
    ).exclude(pk=project.pk)[:4]

    context = {
        "project": project,
        "bids": bids,
        "my_bid": my_bid,
        "similar_projects": similar_projects,
        "is_saved": is_saved,
        "bid_count": bids.count(),
    }
    return render(request, "project_detail.html", context)


@login_required(login_url='login')
def DeleteProjectView(request, id):
    user = request.user
    if user.role != 'client':
        return redirect('login')

    project = get_object_or_404(Project, id=id, client=user)

    if project.status != Project.OPEN:
        return render(request, 'project_delete.html', {
            "project": project,
            "error": "Faqat open loyihani o'chirish mumkin",
        })

    if request.method == "POST":
        project.delete()
        flash.success(request, "Loyiha o'chirildi.")
        return redirect("myprojects")

    return render(request, "project_delete.html", {"project": project})


@login_required(login_url='login')
def EditProjectView(request, id):
    user = request.user
    if user.role != 'client':
        return redirect('login')

    project = get_object_or_404(Project, id=id, client=user)

    if project.status != Project.OPEN:
        return render(request, "edit_project.html", {
            "project": project,
            "error": "Faqat open loyihani tahrirlash mumkin",
        })

    if request.method == "POST":
        project.title = request.POST.get("title") or project.title
        project.description = request.POST.get("description") or project.description
        project.category = request.POST.get("category") or project.category
        project.budget_type = request.POST.get("budget_type") or project.budget_type

        budget_min = request.POST.get("budget_min")
        budget_max = request.POST.get("budget_max")
        if budget_min:
            project.budget_min = budget_min
        if budget_max:
            project.budget_max = budget_max

        project.level = request.POST.get("level") or project.level
        project.skills = request.POST.get("skills") or project.skills

        deadline = request.POST.get("deadline")
        if deadline:
            project.deadline = deadline

        project.save()
        flash.success(request, "Loyiha yangilandi.")
        return redirect("project_detail", id=project.id)

    return render(request, "edit_project.html", {"project": project})


@login_required(login_url='login')
def toggle_save(request, id):
    project = get_object_or_404(Project, id=id)
    if request.user.role != 'freelancer':
        flash.error(request, "Faqat freelancerlar loyihalarni saqlay oladi.")
        return redirect('project_detail', id=id)

    saved = SavedProject.objects.filter(user=request.user, project=project).first()
    if saved:
        saved.delete()
        flash.info(request, "Saqlangan loyihalardan olib tashlandi.")
    else:
        SavedProject.objects.create(user=request.user, project=project)
        flash.success(request, "Loyiha saqlandi.")
    return redirect('project_detail', id=id)


@login_required(login_url='login')
def saved_projects(request):
    qs = SavedProject.objects.filter(user=request.user).select_related('project', 'project__client')
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'saved_projects.html', {'saved': page, 'page_obj': page})
