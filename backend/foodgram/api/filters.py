import django_filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class IngredientSearchFilter(SearchFilter):
    """Фильтр для ингредиентов с переопределенным именем параметра запроса."""

    search_param = 'name'


class RecipeFilter(django_filters.FilterSet):
    """Кастомный фильтр для вьюсета 'Recipe'."""

    author = django_filters.CharFilter(
        field_name='author__id',
        lookup_expr='iexact'
    )
    tags = django_filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='iexact'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
