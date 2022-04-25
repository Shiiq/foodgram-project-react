from django.db import models
from django.db.models import Exists, OuterRef, F, Q, Value

from users.models import User


class RecipeQuerySet(models.QuerySet):
    def is_favorite(self, user):
        if not isinstance(user, User) or not user.is_authenticated:
            return self.annotate(if_favorite=F(False))
        return self.annotate(is_favorite=Exists(self.filter(
            Q(recipe_favorite__recipe=OuterRef('pk')) & Q(recipe_favorite__user=user)
        )))

    def is_in_shopping_cart(self, user):
        if not isinstance(user, User) or not user.is_authenticated:
            return self.annotate(if_favorite=F(False))
        return self.annotate(is_in_shopping_cart=Exists(self.filter(
            Q(in_shopping_cart__recipe=OuterRef('pk')) & Q(in_shopping_cart__user=user)
        )))


class RecipeManager(models.Manager):
    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    def is_favorite(self, user):
        return self.get_queryset().is_favorite(user)

    def is_in_shopping_cart(self, user):
        return self.get_queryset().is_in_shopping_cart(user)
