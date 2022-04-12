from rest_framework import serializers

from recipes.models import Ingredient, Tag, Recipe, RecipeIngredients


class IngredientsSerializer(serializers.ModelSerializer):
    """Выводит информацию о доступных ингредиентах."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientDetailSerializer(serializers.ModelSerializer):
    """Выводит детальную информацию по ингридиентам внутри рецепта."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    ingredient = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'ingredient', 'measurement_unit', 'amount')


class TagsSerializer(serializers.ModelSerializer):
    """Выводит информацию о доступных тегах."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipesShortInfoSerializer(serializers.ModelSerializer):
    """Выводит краткую информацию о рецептах."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


