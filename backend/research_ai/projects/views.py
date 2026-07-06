from django.shortcuts import render, redirect
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
            return redirect("projects")
    else:
        form = ProjectForm()
    return render(request, "projects/create_project.html", {"form": form})