from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.db.models import Count
from django.http import FileResponse
from rest_framework import filters, views, viewsets, status, response, permissions, pagination

from .permissions import IsAuthorOrReadOnly
from .viewsets import ReadOnlyViewSet, ListViewSet
from .serializers import RecipesSerializer, SubscribeSerializer, RecipesCreateSerializer
from .simple_serializers import IngredientsSerializer, TagsSerializer, RecipesShortInfoSerializer
from .utils import get_header_message, get_total_list

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
    pagination_class = pagination.LimitOffsetPagination

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.permission_classes = [permissions.AllowAny, ]
        elif self.action in ('partial_update', 'destroy'):
            self.permission_classes = [IsAuthorOrReadOnly, ]
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
        ).annotate(
            recipes_count=Count('recipes')
        )
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


class DownloadShoppingCart(views.APIView):
    """Обработка запроса на скачивание списка покупок."""
    def get(self, request):
        user = request.user
        carts = user.shopping_cart.select_related('recipe').all()
        message = get_header_message(carts)
        total_list = get_total_list(carts)

        with open('total_list', 'w', encoding='utf-8') as f:
            f.write(f'{message}\n\n')
            for k, v in total_list.items():
                for unit, amount in v.items():
                    f.write(f'{k}: {amount} {unit}\n')

        user.shopping_cart.all().delete()

        response = FileResponse(open('total_list', 'rb'), as_attachment=True)
        return response
