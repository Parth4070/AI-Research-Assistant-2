from django.urls import path
from .views import train_model_view

urlpatterns = [
    path('<int:dataset_id>/train/', train_model_view, name="train_model")
]
