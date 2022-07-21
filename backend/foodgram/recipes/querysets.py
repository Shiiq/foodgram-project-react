from django.db import models
from django.db.models import BooleanField, Exists, OuterRef, Q, Value
from users.models import User


class RecipeQuerySet(models.QuerySet):
    """
    Кастомный queryset для модели Recipe.
    Добавлены поля 'is_favorited' и 'is_in_shopping_cart'.
    """

    def annotated(self, user):
        """Ожидает на вход экземпляр модели 'user'."""

        # Проверяем все возможные ситуации с параметром 'user'.
        if (not isinstance(user, User)
                or user is None
                or not user.is_authenticated):
            return self.annotate(
                is_favorited=Value(False, output_field=BooleanField()),
                is_in_shopping_cart=Value(False, output_field=BooleanField())
            )
        return self.annotate(
            is_favorited=Exists(
                self.filter(
                    # Существует ли связка рецепт-любимый рецепт-юзер.
                    Q(recipe_favorite__recipe=OuterRef('pk'))
                    & Q(recipe_favorite__user=user)
                )),
            is_in_shopping_cart=Exists(
                self.filter(
                    # Существует ли связка рецепт-корзина-юзер.
                    Q(in_shopping_cart__recipe=OuterRef('pk'))
                    & Q(in_shopping_cart__user=user)
                ))
        )


class RecipeManager(models.Manager):
    """
    Кастомный менеджер для queryset'а Recipe.
    Метод annotated() принимает в качестве аргумента экземпляр юзера,
    либо None по умолчанию.
    Дальнейшая проверка юзера реализована в RecipeQueryset.
    """

    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    def annotated(self, user=None):
        return self.get_queryset().annotated(user)
