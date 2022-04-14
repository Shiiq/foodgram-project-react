def get_header_message(queryset):
    """Готовит заголовок для файла списка покупок."""

    recipes_list = (", ".join([cart.recipe.name for cart in queryset]))
    return f'Вы добавили в корзину ингредиенты для: {recipes_list}.'

def get_total_list(queryset):
    """Формирует словарь списка покупок."""

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
