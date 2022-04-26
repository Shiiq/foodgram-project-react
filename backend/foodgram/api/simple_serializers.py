import base64
import re
import time as t

from django.conf import settings
from django.utils.text import slugify
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredients, Tag


class IngredientsSerializer(serializers.ModelSerializer):
    """Выводит информацию о доступных ингредиентах."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientDetailSerializer(serializers.ModelSerializer):
    """Выводит детальную информацию по ингридиентам внутри рецепта."""

    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    ingredient = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

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


class Base64toImageFile(serializers.Field):
    """
    Обработка данных из поля image с последующим
    сохранением изображения в БД.
    """

    pattern = (
        r'data:(?P<f_dir>\w+)\/(?P<f_ext>\w+);base64,(?P<byte_string>.+)'
    )

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        """
        Название изображения формируется
        из хеша временной метки и названия рецепта.
        При PATCH запросе старое изображение удаляется.
        """

        recipe_name = self.context['request'].data['name']
        slugify_name = slugify(recipe_name, allow_unicode=True)
        to_compile = re.compile(self.pattern)
        parse = to_compile.search(data)
        f_dir = parse.group('f_dir')
        f_ext = parse.group('f_ext')
        byte_string = parse.group('byte_string')

        f_name = f'{hash(t.time())}-{slugify_name}.{f_ext}'
        to_bytes = base64.b64decode(byte_string)

        with open(
            f'{settings.MEDIA_ROOT}\\recipes\\{f_dir}\\{f_name}',
            'wb'
        ) as im:
            im.write(to_bytes)

        return f'recipes/images/{f_name}'
