from recipes.models import Ingredient, Tag, Recipe, RecipeIngredients, RecipeTags
from rest_framework import viewsets
from .serializers import IngredientsSerializer, TagsSerializer, RecipesSerializer
from .pagination import IngredientsPagination
from rest_framework import filters


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Обработка запросов к ингрeдиентам"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = IngredientsPagination
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['^name', ]


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer


