from django.shortcuts import get_object_or_404
from rest_framework import filters, views, viewsets, status, response, permissions
from django.db import IntegrityError

from .viewsets import ReadOnlyViewSet, ListViewSet
from .serializers import RecipesSerializer, SubscribeSerializer, RecipesCreateSerializer
from .simple_serializers import IngredientsSerializer, TagsSerializer, RecipesShortInfoSerializer

from recipes.models import Ingredient, Tag, Recipe, RecipeIngredients, RecipeTags, RecipeFavorite, ShoppingCart
from users.models import User, Subscription


class IngredientsViewSet(ReadOnlyViewSet):
    """Обработка запросов к ингрeдиентам."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['^name', ]


class TagsViewSet(ReadOnlyViewSet):
    """Обработка запросов к тегам."""
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Обработка запросов к рецептам."""
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.permission_classes = [permissions.AllowAny, ]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipesCreateSerializer
        return RecipesSerializer


class MakeSubscription(views.APIView):
    """Обработка запросов на подписку/отписку."""

    def post(self, request, id):
        author = get_object_or_404(User, id=id)
        try:
            Subscription.objects.create(
                author=author, subscriber=request.user
            )
        except IntegrityError as error:
            return response.Response(
                data={'errors': str(error.__context__)},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SubscribeSerializer(
                author, context={'request': request}
        )
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        Subscription.objects.filter(
            author=author, subscriber=request.user
        ).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ShowSubscriptionViewSet(ListViewSet):
    """Отображает текущие подписки пользователя."""
    queryset = User.objects.all()
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        request_user = self.request.user
        queryset = User.objects.filter(
            subscribers__subscriber=request_user
        ).all()
        return queryset


class AddToFavorite(views.APIView):
    """
    Обработка запросов на добавление/удаление
    рецепта в избранное.
    """

    def post(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        try:
            RecipeFavorite.objects.create(
                recipe=recipe, user=request.user
            )
        except IntegrityError as error:
            return response.Response(
                data={'errors': str(error.__context__)},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RecipesShortInfoSerializer(
                recipe, context={'request': request}
        )
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        RecipeFavorite.objects.filter(
            recipe=recipe, user=request.user
        ).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class AddToShoppingCart(views.APIView):
    """
    Обработка запросов на добавление/удаление
    рецепта в корзину покупок.
    """

    def post(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        try:
            ShoppingCart.objects.create(
                recipe=recipe, user=request.user
            )
        except IntegrityError as error:
            return response.Response(
                data={'errors': str(error.__context__)},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RecipesShortInfoSerializer(
                recipe, context={'request': request}
        )
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        RecipeFavorite.objects.filter(
            recipe=recipe, user=request.user
        ).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
