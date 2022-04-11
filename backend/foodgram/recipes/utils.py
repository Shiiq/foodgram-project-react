import os
from django.utils.text import slugify


def get_upload_path(instance, filename):
    """Формирует путь хранения изображений."""
    #filename = str(hash(filename)).strip('-')
    dirname = slugify(
        (instance.id, instance.name),
        allow_unicode=True
    )
    return os.path.join(
        'recipes',
        dirname,
        filename
    )
