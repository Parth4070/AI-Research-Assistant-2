from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
@login_required
def projects_list(request):
    projects = Projects.objects.filter(owner=request.user)
    return render(request, "projects/projects.html", {"projects": projects})


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect("projects_list")
    else:
        form = ProjectForm()
    return render(request, "projects/create_project.html", {"form": form})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Projects, id=project_id, owner=request.user)
    datasets = project.datasets.all()
    context = {
        "project": project,
        "dataset": datasets
    }
    return render(request, "projects/project_detail.html", context)
