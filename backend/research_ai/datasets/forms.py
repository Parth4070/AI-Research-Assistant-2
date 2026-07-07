from django import forms
from .models import *

class DatasetUploadForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ["name" ,"file"]
