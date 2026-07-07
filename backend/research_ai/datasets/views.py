from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from projects.models import Projects
from .forms import DatasetUploadForm
import pandas as pd
from .models import *

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

            return redirect("dataset_detail", dataset.id)

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

@login_required
def dataset_detail(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id, project__owner=request.user)

    data_path = dataset.file.path

    if data_path.endswith(".csv"):
        df = pd.read_csv(data_path)

    elif data_path.endswith(".xlsx"):
        df = pd.read_excel(data_path)
    
    else:
        df = None
    
    context = {
        "dataset" : dataset,
        "rows" : df.shape[0],
        "columns": df.shape[1],
        "column_names" : df.columns.tolist()
    }

    return render(request, "datasets/detail.html", context)