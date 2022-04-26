from django.db import models
from django.db.models import BooleanField, Exists, OuterRef, Q, Value

from users.models import User


class RecipeQuerySet(models.QuerySet):
    """Кастомный queryset для модели Recipe."""

    def annotated(self, user):
        if not isinstance(user, User) or user is None or not user.is_authenticated:
            return self.annotate(
                is_favorited=Value(False, output_field=BooleanField()),
                is_in_shopping_cart=Value(False, output_field=BooleanField())
            )
        return self.annotate(
            is_favorited=Exists(
                self.filter(Q(recipe_favorite__recipe=OuterRef('pk')) &
                            Q(recipe_favorite__user=user))
            ),
            is_in_shopping_cart=Exists(
                self.filter(Q(in_shopping_cart__recipe=OuterRef('pk')) &
                            Q(in_shopping_cart__user=user))
            )
        )


class RecipeManager(models.Manager):
    """
    Кастомный менеджер для queryset'а Recipe.
    Метод annotated() принимает в качестве аргумента экземпляр юзера,
    либо подставляет значение None при его отсутствии.
    Дальнейшая проверка юзера проводится в самом RecipeQueryset.
    """

    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    # def get_queryset(self, user=None):
    #     qs = super(RecipeManager, self).get_queryset()
    #     return qs.annotated(user)

    def annotated(self, user=None):
        return self.get_queryset().annotated(user)
