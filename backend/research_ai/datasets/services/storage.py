from io import StringIO
from django.core.files.base import ContentFile


def dataframe_to_contentfile(df):
    """
    Converts Pandas DataFrame to Django ContentFile.
    """
    buffer = StringIO()
    df.to_csv(buffer, index=False)
    return ContentFile(buffer.getvalue())