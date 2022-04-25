from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.utils import delete_recipe_image
from recipes.models import (Ingredient, Recipe, RecipeFavorite,
                            RecipeIngredients, ShoppingCart, Tag)
from users.models import Subscription

from .simple_serializers import (Base64toImageFile, IngredientDetailSerializer,
                                 RecipesShortInfoSerializer)

User = get_user_model()


class CustomUsersSerializer(UserSerializer):
    """Для вывода информации о пользователе."""

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(
                author=obj,
                user=user
            ).exists()
        return False

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


class RecipesSerializer(serializers.ModelSerializer):
    """Выводит информацию о рецептах."""

    ingredients = IngredientDetailSerializer(
        source='recipe_ingredients',
        many=True
    )
    author = CustomUsersSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return RecipeFavorite.objects.filter(
                recipe=obj,
                user=user
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                recipe=obj,
                user=user
            ).exists()
        return False

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'tags',
            'ingredients', 'text',
            'cooking_time', 'author',
            'is_favorited', 'is_in_shopping_cart'
        )
        depth = 1


class IngredientsToWrite(serializers.ModelSerializer):
    """
    Используется для записи информации
    об ингредиентах при создании рецепта.
    """

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.FloatField(required=True)

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


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
        super().update(instance=instance, validated_data=validated_data)

        delete_recipe_image(instance.image.path)

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
