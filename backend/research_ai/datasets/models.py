from django.forms.models import ModelFormOptions
from django.db import models
from projects.models import Projects

# Create your models here.
class Dataset(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="datasets")
    file = models.FileField(upload_to="datasets/")
    name = models.CharField(max_length=300, default="")
    is_original = models.BooleanField(default=True)
    parent_dataset = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="derived_datasets"
    )
    processing_step = models.CharField(max_length=100, default="Original")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.file.name.split("/")[-1]

        