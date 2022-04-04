from recipes.models import Ingredient, Tag, Recipe, RecipeIngredients, RecipeTags
from rest_framework import serializers


class IngredientsSerializer(serializers.ModelSerializer):
    """Обслуживает модель Ingredient."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagsSerializer(serializers.ModelSerializer):
    """Обслуживает модель Tag."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientDetailSerializer(serializers.ModelSerializer):
    """Выводит точную информацию по ингридиентам."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    ingredient = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'ingredient', 'measurement_unit', 'value')


class RecipesSerializer(serializers.ModelSerializer):
    """Обслуживает модель Recipe."""
    ingredient = IngredientDetailSerializer(source="RecipeIngredients", many=True)
    # print(Recipe.objects.get(pk=2).ingredient.first().name)
    # print(Ingredient.objects.get(pk=2177).recipes.all())
    # print(Recipe.objects.filter(ingredient__id=2177))
    # print(Ingredient.objects.filter(recipes__name__startswith='Стейк'))
    # for i in RecipeIngredients.objects.filter(recipe__in=Recipe.objects.all()):
    #     print(i.ingredient, i.value)
    # print(RecipeIngredients.objects.filter(recipe__in=Recipe.objects.all()).value.all())

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'tag',
            'ingredient', 'description',
            'cooking_time'
        )
        depth = 1
