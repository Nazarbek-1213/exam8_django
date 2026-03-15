from django.shortcuts import render, redirect, get_object_or_404

from Bid.models import Bid
from .forms import ProjectForm
from .models import Project

def CreateProView(request):
    if request.user.role != 'client':
        return redirect('main_freelancer')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        print("IS VALID:", form.is_valid())
        print("ERRORS:", form.errors)
        print("POST DATA:", request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.status = 'open'
            project.save()
            return redirect('main_client')
    else:
        form = ProjectForm()

    return render(request, 'create_post.html', {'form': form})

def SelfProjectsView(request):
    user = request.user

    projects = Project.objects.filter(client=user).order_by('-created_at')

    context = {
        'projects': projects
    }

    return render(request, 'myprojects.html', context)



def ProjectdetailsView(request, id):
    user = request.user

    if user.role != 'client':
        return redirect('login')

    project = get_object_or_404(Project, id=id, client=user)

    bids = Bid.objects.filter(project=project)

    freelancers = []
    durations = []

    for bid in bids:

        if hasattr(bid, "freelancer") and bid.freelancer:
            freelancers.append(str(bid.freelancer))

        if getattr(bid, "finished_at", None):
            durations.append(bid.finished_at - bid.created_at)

    context = {
        "project": project,
        "bids": bids,
        "freelancers": freelancers,
        "durations": durations
    }

    return render(request, "project_detail.html", context)



def DeleteProjectView(request, id):
    user = request.user

    if user.role != 'client':
        return redirect('login')

    project = get_object_or_404(Project, id=id, client=user)

    if project.status != Project.OPEN:
        return render(request, 'project_delete.html', {
            "project": project,
            "error": "Faqat open loyihani o'chirish mumkin"
        })

    if request.method == "POST":
        project.delete()
        return redirect("myprojects")

    return render(request, "project_delete.html", {"project": project})



def EditProjectView(request, id):
    user = request.user

    if user.role != 'client':
        return redirect('login')

    project = get_object_or_404(Project, id=id, client=user)

    if project.status != Project.OPEN:
        return render(request, "edit_project.html", {
            "project": project,
            "error": "Faqat open loyihani tahrirlash mumkin"
        })

    if request.method == "POST":

        project.title = request.POST.get("title")
        project.description = request.POST.get("description")

        project.category = request.POST.get("category")

        project.budget_type = request.POST.get("budget_type")
        project.budget_min = request.POST.get("budget_min")
        project.budget_max = request.POST.get("budget_max")

        project.level = request.POST.get("level")
        project.skills = request.POST.get("skills")

        project.deadline = request.POST.get("deadline")

        project.save()

        return redirect("project_detail", id=project.id)

    return render(request, "edit_project.html", {"project": project})