from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Пользовательская модель юзера с переопределенными полями."""
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    first_name = models.CharField(max_length=150)

    """
    A string describing the name of the field on the user model
    that is used as the unique identifier.
    This will usually be a username of some kind,
    but it can also be an email address, or any other unique identifier.
    The field must be unique (i.e., have unique=True set in its definition),
    unless you use a custom authentication backend that can support non-unique usernames.
    """
    USERNAME_FIELD = 'email'

    """
    A list of the field names that will be prompted for
    when creating a user via the createsuperuser management command.
    The user will be prompted to supply a value for each of these fields.
    It must include any field for which blank is False or undefined and
    may include additional fields you want prompted for when a user is created interactively. 
    REQUIRED_FIELDS has no effect in other parts of Django, like creating a user in the admin.
    """
    REQUIRED_FIELDS = ['username']
