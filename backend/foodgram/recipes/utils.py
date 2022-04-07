import os


def get_upload_path(instance, filename):
    """Формирует путь хранения изображений."""
    return os.path.join(
        'recipes',
        f'{instance.id}_{instance.name}',
        filename
    )
