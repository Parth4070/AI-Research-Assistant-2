from io import StringIO
from django.core.files.base import ContentFile
from .pipeline import generate_clean_filename
from datasets.models import Dataset

class DatasetService:
    @staticmethod
    def create_clean_version(og_dataset, clean_df):
        buffer = StringIO()
        clean_df.to_csv(buffer, index = False)
        content = ContentFile(buffer.getvalue())
        filename = generate_clean_filename(og_dataset)

        new_dataset = Dataset.objects.create(
            project=og_dataset.project,
            name=f"{og_dataset.name} (Cleaned)",
            is_original=False,
            processing_step="Cleaning"
        )

        new_dataset.file.save(filename,content)

        return new_dataset
    