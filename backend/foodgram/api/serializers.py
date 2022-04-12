from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer

from .simple_serializers import IngredientDetailSerializer, RecipesShortInfoSerializer
from recipes.models import Ingredient, Tag, Recipe, RecipeIngredients, RecipeTags, RecipeFavorite, ShoppingCart
from users.models import Subscription

User = get_user_model()


class CustomUsersSerializer(UserSerializer):
    """Для вывода информации о пользователе."""
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return False
        return Subscription.objects.filter(
            author=obj, subscriber=request_user
        ).exists()

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

    def get_is_favorited(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return False
        return RecipeFavorite.objects.filter(
            recipe=obj, user=request_user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            recipe=obj, user=request_user
        ).exists()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'tags',
            'ingredients', 'text',
            'cooking_time', 'author',
            'is_favorited', 'is_in_shopping_cart'
        )
        depth = 1


class SubscribeSerializer(CustomUsersSerializer):
    """Выводит список авторов, на которых подписан пользователь."""
    recipes = RecipesShortInfoSerializer(many=True)
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


class IngredientsToWrite(serializers.ModelSerializer):
    """Используется для записи информации об ингредиентах при создании рецепта."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), required=True
    )
    amount = serializers.FloatField(required=True)

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class RecipesCreateSerializer(serializers.ModelSerializer):
    """Используется на запись и редактирование при создании рецепта."""
    author = CustomUsersSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientsToWrite(required=True, many=True)
    # image =

    def to_representation(self, instance):
        return RecipesSerializer(instance, context=self.context).data

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)

        for tag in tags:
            recipe.tags.add(tag)

        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                value=ingredient['amount']
            )

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.save()

        for tag in tags:
            instance.tags.add(tag)

        instance.recipe_ingredients.all().delete()
        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                recipe=instance,
                ingredient=ingredient['id'],
                value=ingredient['amount']
            )

        return instance

    class Meta:
        model = Recipe
        fields = (
            'author', 'name', 'cooking_time',
            'tags', 'text', 'ingredients'
        )
