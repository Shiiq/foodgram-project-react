import os
from django.utils.text import slugify


def get_upload_path(instance, filename):
    """Формирует путь хранения изображений."""
    file_extension = os.path.splitext(filename)[1]
    file_name = slugify(
        (instance.id, instance.name),
        allow_unicode=True
    )
    return f'{file_name}{file_extension}'
