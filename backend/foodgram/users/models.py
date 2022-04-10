from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import AbstractUser

from recipes.models import Recipe


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

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    """Подписка."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор'
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name='Подписчик'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.CheckConstraint(
                check=~Q(subscriber=F('author')),
                name='subscriber_not_equal_author'
            ),
            models.UniqueConstraint(
                fields=['author', 'subscriber'],
                name='unique_subscription')
        ]

    def __str__(self):
        author = self.author.username
        subscriber = self.subscriber.username
        return f'{subscriber} подписан на {author}'


class RecipeFavorite(models.Model):
    """Избранные рецепты. Связка рецепт-пользователь."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_favorite',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_favorite',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_in_favorite')
        ]

    def __str__(self):
        user = self.user.username
        recipe = self.recipe.name
        return f'{user} добавил "{recipe}" в избранное'
