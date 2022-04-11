from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from recipes.models import Ingredient, Tag, Recipe, RecipeIngredients, RecipeTags
from users.models import Subscription, RecipeFavorite

User = get_user_model()


class CustomUsersSerializer(UserSerializer):
    """Отображает информацию о пользователе."""
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return False
        return Subscription.objects.filter(
            author=obj,
            subscriber=request_user
        ).exists()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed'
        )


class CustomUsersCreateSerializer(UserCreateSerializer):
    """Создает пользователя."""
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password',
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
        fields = ('id', 'ingredient', 'measurement_unit', 'value')


class RecipesSerializer(serializers.ModelSerializer):
    """Обслуживает модель Recipe."""
    ingredients = IngredientDetailSerializer(
        source='recipe_ingredients',
        many=True
    )
    author = CustomUsersSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return False
        return RecipeFavorite.objects.filter(
            recipe=obj,
            user=request_user
        ).exists()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'tags',
            'ingredients', 'text',
            'cooking_time', 'author',
            'is_favorited'
        )
        depth = 1


class RecipesDisplaySerializer(serializers.ModelSerializer):
    """Используется как вложенный сериалайзер."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(CustomUsersSerializer):
    recipes = RecipesDisplaySerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'recipes',
            'recipes_count'
        )


# class IngredientsToWrite(serializers.ModelSerializer):
#     id = serializers.IntegerField(required=True, source='ingredient.id')
#     value = serializers.FloatField(required=True)
#
#     class Meta:
#         model = RecipeIngredients
#         fields = ('id', 'value')


class IngredientsToWrite(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    value = serializers.FloatField(required=True)


class RecipesCreateSerializer(serializers.ModelSerializer):
    """Для записи рецепта в БД."""
    author = CustomUsersSerializer(
        read_only=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientsToWrite(
        required=True,
        many=True)
    # image =

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            **validated_data,
            author=author
        )
        # for tag in tags:
        #     recipe.tags.add(tag)
        for ingredient in ingredients:
            print(ingredient['id'])
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient__id=ingredient['id'],
                value=ingredient['value']
            )
        # return recipe
        # pass


    class Meta:
        model = Recipe
        fields = (
            'author', 'name', 'cooking_time',
            'tags', 'text', 'ingredients'
        )
