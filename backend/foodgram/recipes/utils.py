import os
from django.db import models


def get_upload_path(instance, filename):
    return os.path.join(
        'recipes',
        f'{instance.id}_{instance.name}',
        filename
    )
