import base64
import re
import time as t

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils.text import slugify
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recipe, RecipeIngredients, Tag
from .simple_serializers import (IngredientDetailSerializer,
                                 IngredientsToWrite,
                                 RecipesShortInfoSerializer)

User = get_user_model()


class CustomUsersSerializer(UserSerializer):
    """Для вывода информации о пользователе."""

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated
                and obj.subscribers.filter(user=user).exists())

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed'
        )


class CustomUsersCreateSerializer(UserCreateSerializer):
    """Для регистрации пользователя."""

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password'
        )


class Base64toImageFile(serializers.ImageField):
    """
    Обработка данных из поля image с последующим сохранением изображения в БД.
    При записи в поле поступает байтовая строка,
    которая декодируется в изображение и сохраняется.
    При просмотре возвращается url изображения.
    """

    pattern = (
        r'data:(?P<f_dir>\w+)\/(?P<f_ext>\w+);base64,(?P<byte_string>.+)'
    )

    def to_representation(self, value):
        return value.url

    def to_internal_value(self, data):
        """
        Название изображения формируется
        из хеша временной метки и слага названия рецепта.
        Если при редактировании рецепта заменяется изображение,
        то старое изображение удаляется.
        """

        recipe_name = self.context['request'].data['name']
        slugify_name = slugify(recipe_name, allow_unicode=True)
        to_compile = re.compile(self.pattern)
        parse = to_compile.search(data)
        f_ext = parse.group('f_ext')
        byte_string = parse.group('byte_string')
        f_name = f'{hash(t.time())}-{slugify_name}.{f_ext}'
        decoded_byte_string = base64.b64decode(byte_string)

        image = ContentFile(decoded_byte_string, name=f_name)
        return super(Base64toImageFile, self).to_internal_value(image)


class RecipesSerializer(serializers.ModelSerializer):
    """Выводит информацию о рецептах."""

    ingredients = IngredientDetailSerializer(
        source='recipe_ingredients',
        many=True
    )
    author = CustomUsersSerializer(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    image = Base64toImageFile()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'tags',
            'ingredients', 'text',
            'cooking_time', 'author',
            'is_favorited', 'is_in_shopping_cart'
        )
        depth = 1


class RecipesCreateSerializer(serializers.ModelSerializer):
    """Используется на запись и редактирование рецепта."""

    author = CustomUsersSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientsToWrite(
        required=True,
        many=True
    )
    image = Base64toImageFile(required=True)

    def to_representation(self, instance):
        return RecipesSerializer(instance, context=self.context).data

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)

        recipe.tags.set(tags)

        recipe_ingredients = [RecipeIngredients(
            recipe=recipe,
            ingredient=ingredient['id'],
            amount=ingredient['amount']
        ) for ingredient in ingredients]
        RecipeIngredients.objects.bulk_create(recipe_ingredients)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        if validated_data.get('image') is not None:
            instance.image.delete()

        super().update(instance=instance, validated_data=validated_data)

        instance.tags.set(tags)

        instance.recipe_ingredients.all().delete()
        recipe_ingredients = [RecipeIngredients(
            recipe=instance,
            ingredient=ingredient['id'],
            amount=ingredient['amount']
        ) for ingredient in ingredients]
        RecipeIngredients.objects.bulk_create(recipe_ingredients)

        return instance

    class Meta:
        model = Recipe
        fields = (
            'author', 'name', 'cooking_time',
            'tags', 'text', 'ingredients',
            'image'
        )


class SubscribeSerializer(CustomUsersSerializer):
    """Выводит список авторов, на которых подписан пользователь."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField()

    def get_recipes(self, obj):
        request = self.context['request']
        recipes_limit = request.query_params.get('recipes_limit')
        recipes = obj.recipes.all()

        if recipes_limit is None:
            return RecipesShortInfoSerializer(recipes, many=True).data
        elif not recipes_limit.isnumeric():
            raise serializers.ValidationError(
                'Проверьте значение параметра recipes_limit!'
            )

        recipes = obj.recipes.all()[:int(recipes_limit)]
        return RecipesShortInfoSerializer(recipes, many=True).data

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'recipes',
            'recipes_count'
        )
