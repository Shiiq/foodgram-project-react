import os
import time as t

from django.utils.text import slugify


def get_upload_path(instance, filename):
    """
    Формирует путь хранения изображений при добавлении через админку.
    Название изображения формируется из хеша временной метки
    и названия рецепта.
    """

    slugify_name = slugify(instance.name, allow_unicode=True)
    f_ext = os.path.splitext(filename)[1]
    f_name = f'{hash(t.time())}-{slugify_name}{f_ext}'
    return os.path.join('recipes', 'images', f'{f_name}')
