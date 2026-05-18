from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from Bid.models import Bid
from .forms import ProjectForm
from .models import Project


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
            return redirect('main_client')
    else:
        form = ProjectForm()

    return render(request, 'create_post.html', {'form': form})


@login_required(login_url='login')
def SelfProjectsView(request):
    user = request.user

    projects = Project.objects.filter(client=user).order_by('-created_at')

    context = {
        'projects': projects,
    }

    return render(request, 'myprojects.html', context)


@login_required(login_url='login')
def ProjectdetailsView(request, id):
    user = request.user

    project = get_object_or_404(Project, id=id)

    bids = Bid.objects.filter(project=project).select_related('freelancer')

    my_bid = None
    if user.role == 'freelancer':
        my_bid = Bid.objects.filter(
            project=project,
            freelancer=user,
        ).first()

    similar_projects = Project.objects.filter(
        category=project.category,
    ).exclude(pk=project.pk)[:4]

    context = {
        "project": project,
        "bids": bids,
        "my_bid": my_bid,
        "similar_projects": similar_projects,
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

        return redirect("project_detail", id=project.id)

    return render(request, "edit_project.html", {"project": project})
