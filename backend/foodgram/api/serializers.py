from recipes.models import Ingredient, Tag, Recipe, RecipeIngredients, RecipeTags
from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

User = get_user_model()


class UsersSerializer(UserCreateSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email', 'username',
            'first_name', 'last_name',
            'password'
        )


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


# "email": "user@example.com",
# "id": 0,
# "username": "string",
# "first_name": "Вася",
# "last_name": "Пупкин",
# "is_subscribed": false
# class UsersSerializer(serializers.ModelSerializer):
#     # is_subscribed = serializers.SerializerMethodField(
#     #     read_only=True
#     # )
#     class Meta:
#         model = User
#         fields = (
#             'email', 'id', 'username',
#             'first_name', 'last_name',
#             # 'is_subscribed'
#         )


class RecipesSerializer(serializers.ModelSerializer):
    """Обслуживает модель Recipe."""
    ingredients = IngredientDetailSerializer(source="RecipeIngredients", many=True)
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
            'id', 'name', 'image', 'tags',
            'ingredients', 'text',
            'cooking_time', 'author'
        )
        depth = 1
