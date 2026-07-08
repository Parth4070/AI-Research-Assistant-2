from django.urls import path
from . import views

urlpatterns = [
    path("<int:project_id>/upload-dataset/", views.upload_dataset, name="upload_dataset"),
    path("<int:dataset_id>/", views.dataset_detail, name="dataset_detail"),
    path("<int:dataset_id>/clean/", views.clean_dataset_view, name="clean_dataset")
]