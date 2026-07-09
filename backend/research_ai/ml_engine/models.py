from django.db import models
from datasets.models import Dataset

# Create your models here.
class MLExpriment(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="experiments")
    target_column = models.CharField(max_length=100)
    problem_type = models.CharField(max_length=100)
    best_model = models.CharField(max_length=100)
    accuracy =  models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    model_file = models.FileField(upload_to="models/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.best_model} - {self.dataset.name}"