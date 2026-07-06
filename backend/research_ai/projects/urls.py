from django.urls import path
from .views import *

urlpatterns = [
    path("", projects_list, name="projects_list"),
    path("create/", create_project, name="create_project"),
]
