from django.db import models
from django.db.models import Exists, OuterRef, F

# from users.models import User
#
#
# class RecipeQuerySet(models.QuerySet):
#     # qs = self.select_related('recipe_favorite')
#     def is_favorite(self, user):
#         qs = self.prefetch_related('recipe_favorite')
#         if not isinstance(user, User) or not user.is_authenticated:
#             return self.annotate(if_favorite=False)
#         return qs.annotate(
#             is_favorite=Exists(
#                 qs.recipe_favorite.filter(
#                     recipe=OuterRef('pk'),
#                     user=user
#                 )))
#
#
# class RecipeManager(models.Manager):
#     def get_queryset(self):
#         return RecipeQuerySet(self.model, using=self._db)
#
#     def is_favorite(self, user):
#         return self.get_queryset().is_favorite(user)
