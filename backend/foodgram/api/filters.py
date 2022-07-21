import django_filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class IngredientSearchFilter(SearchFilter):
    """Фильтр для ингредиентов с переопределенным именем параметра запроса."""

    search_param = 'name'


class RecipeFilter(django_filters.FilterSet):
    """
    Кастомный фильтр для вьюсета 'Recipe'.
    Параметры 'is_favorited' и 'is_in_shopping_cart' для удобства
    будут задаваться в строке запроса 1 и 0 вместо True/False.
    """

    CHOICES = (('1', True), ('0', False))

    author = django_filters.CharFilter(field_name='author__id')
    is_favorited = django_filters.ChoiceFilter(
        choices=CHOICES,
        field_name='is_favorited'
    )
    is_in_shopping_cart = django_filters.ChoiceFilter(
        choices=CHOICES,
        field_name='is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'is_in_shopping_cart')
