from .services.pipeline import generate_clean_filename
from .services.pipeline import DataCleaningPipeline
from django.shortcuts import render
from io import StringIO
from django.core.files.base import ContentFile
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .services.profilling import *
from projects.models import Projects
from .forms import DatasetUploadForm
import pandas as pd
from .models import Dataset

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

            dataset.is_original = True
            dataset.processing_step = "Original"
            dataset.save()

            return redirect("dataset_detail", dataset.id)

    else:

        form = DatasetUploadForm()

    datasets = project.datasets.all()

    return render(
        request,
        "datasets/upload.html",
        {
            "form": form,
            "project": project,
            "datasets": datasets
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
    
    profile = profile_dataset(data_path)

    context = {
        "dataset" : dataset,
        **profile
    }

    return render(request, "datasets/detail.html", context)

@login_required
def clean_dataset_view(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id, project__owner=request.user)

    file_path = dataset.file.path

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    
    else:
        raise ValueError("Unsupported file format.")
    
    pipeline = DataCleaningPipeline()

    clean_df, report = pipeline.run(df)
    buffer = StringIO()
    clean_df.to_csv(buffer, index=False)
    content = ContentFile(buffer.getvalue())
    filename = generate_clean_filename(dataset)

    new_dataset = Dataset.objects.create(
        project=  dataset.project,
        name=f"{dataset.name} (Cleaned)",
        is_original=False,
        parent_dataset=dataset,
        processing_step = "Cleaning"
    )
    new_dataset.file.save(filename, content)
    
    return redirect("dataset_detail", new_dataset.id)