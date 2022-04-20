from rest_framework.serializers import ValidationError


def get_header_message(queryset):
    """
    Готовит заголовок из перечня рецептов для списка покупок.
    На вход поступает queryset экземпляров модели ShoppingCart.
    """

    recipes_list = (", ".join([cart.recipe.name for cart in queryset]))
    return f'Вы добавили в корзину ингредиенты для: {recipes_list}.'


def get_total_list(queryset):
    """
    Формирует список покупок.
    На вход поступает queryset экземпляров модели ShoppingCart.
    Структура списка - {'ингредиент': {'ед.изм.': 'количество'}.
    """

    total_list = {}
    for cart in queryset:
        r_ingredients = cart.recipe.recipe_ingredients.all()
        for r_ingredient in r_ingredients:
            name = r_ingredient.ingredient.name
            amount = r_ingredient.amount
            unit = r_ingredient.ingredient.measurement_unit
            if total_list.get(name) is None:
                total_list[name] = {unit: amount}
            else:
                total_list[name][unit] += amount
    return total_list


class IsFavOrInShopCart:
    """
    Вспомогательный класс для реализации фильтров
    'is_favorited' и 'is_in_shopping_cart' со встроенной валидацией
    значения параметра.
    """

    values = {
        '0': False,
        '1': True
    }

    def __init__(self, value, name):
        self.name = name
        if value not in self.values:
            raise ValidationError(
                f'Параметр {name} может принимать значения 0 или 1!'
            )
        else:
            self.value = value

    @property
    def check(self):
        """При значении True фильтр будет активен."""
        return self.values[self.value]
