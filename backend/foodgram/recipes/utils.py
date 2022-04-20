import os

from django.utils.text import slugify


def get_upload_path(instance, filename):
    """Формирует путь хранения изображений."""

    f_name = slugify(instance.name, allow_unicode=True)
    f_extension = os.path.splitext(filename)[1]
    return os.path.join('recipes/images', f'{f_name}{f_extension}')
