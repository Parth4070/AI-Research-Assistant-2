from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from projects.models import Projects
from .forms import DatasetUploadForm


@login_required
def upload_dataset(request, project_id):

    project = get_object_or_404(
        Projects,
        id=project_id,
        owner=request.user
    )

    if request.method == "POST":

        form = DatasetUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            dataset = form.save(commit=False)

            dataset.project = project

            dataset.save()

            return redirect("project_detail", project.id)

    else:

        form = DatasetUploadForm()

    return render(
        request,
        "datasets/upload.html",
        {
            "form": form,
            "project": project
        }
    )