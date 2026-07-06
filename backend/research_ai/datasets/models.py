from django.db import models
from projects.models import Projects

# Create your models here.
class Dataset(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="datasets")
    file = models.FileField(upload_to="datasets/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    