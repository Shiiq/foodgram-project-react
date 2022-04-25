from django.db import IntegrityError
from django.db.models import Count, Q, Prefetch
from django.apps import apps
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, status, views, viewsets
from rest_framework.response import Response

from recipes.models import (Ingredient, Recipe, RecipeFavorite, ShoppingCart,
                            Tag)
from users.models import Subscription, User

from .filters import IngredientSearchFilter, RecipeFilter
from .permissions import RecipePermission
from .serializers import (RecipesCreateSerializer, RecipesSerializer,
                          SubscribeSerializer)
from .simple_serializers import (IngredientsSerializer,
                                 RecipesShortInfoSerializer, TagsSerializer)
from .utils import IsFavOrInShopCart, get_header_message, get_total_list
from .viewsets import ListViewSet, RetrieveListModelViewSet


class IngredientsViewSet(RetrieveListModelViewSet):
    """Обработка запросов к ингрeдиентам."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('^name', )


class TagsViewSet(RetrieveListModelViewSet):
    """Обработка запросов к тегам."""

    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Обработка запросов к рецептам."""

    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (RecipePermission, )
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset

        active_filters = []

        fav_param = self.request.query_params.get('is_favorited', '0')
        is_fav = IsFavOrInShopCart(fav_param, 'is_favorited')
        if is_fav.check:
            active_filters.append(Q(recipe_favorite__user=user))

        cart_param = self.request.query_params.get('is_in_shopping_cart', '0')
        in_shop_cart = IsFavOrInShopCart(cart_param, 'is_in_shopping_cart')
        if in_shop_cart.check:
            active_filters.append(Q(in_shopping_cart__user=user))

        # for i in Recipe.objects.is_favorite(user):
        #     print(i.is_favorite, i.name)
        # for i in Recipe.objects.is_in_shopping_cart(user):
        #     print(i.is_in_shopping_cart, i.name)

        return self.queryset.filter(*active_filters)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipesCreateSerializer
        return RecipesSerializer


class AddToFavOrShopCartCommonView(views.APIView):
    """
    Общий APIView для обработки запросов
    на добавление рецепта в избранное или корзину.
    """

    def post(self, request, id, primary, secondary):
        primary = apps.get_model(primary['app'], primary['model'])
        secondary = apps.get_model(secondary['app'], secondary['model'])
        recipe = get_object_or_404(secondary, id=id)
        # data = {k: v for k, v in zip([f.name for f in primary._meta.get_fields()[1:]], [secondary_unit, request.user])}
        try:
            primary.objects.create(recipe=recipe, user=request.user)

        except IntegrityError as error:
            return Response(
                data={'errors': str(error.__context__)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RecipesShortInfoSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id, primary, secondary):
        primary = apps.get_model(primary['app'], primary['model'])
        secondary = apps.get_model(secondary['app'], secondary['model'])
        recipe = get_object_or_404(secondary, id=id)

        try:
            if not primary.objects.filter(
                    recipe=recipe,
                    user=request.user
            ).exists():
                return Response(
                    data={'errors': 'Такого рецепта нет в избранном или корзине.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            primary.objects.filter(recipe=recipe, user=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as error:
            return Response(
                data={'errors': str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )


class MakeSubscription(views.APIView):
    """Обработка запросов на подписку/отписку."""

    def post(self, request, id):
        author = get_object_or_404(User, id=id)

        try:
            Subscription.objects.create(author=author, user=request.user)

        except IntegrityError as error:
            return response.Response(
                data={'errors': str(error.__context__)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SubscribeSerializer(
            User.objects.annotate(recipes_count=Count('recipes')).get(id=id),
            context={'request': request}
        )
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)

        try:
            if not Subscription.objects.filter(author=author, user=request.user).exists():
                return Response(
                    data={f'errors': f'Вы не подписаны на {author}.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Subscription.objects.filter(
                author=author,
                user=request.user
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as error:
            return Response(
                data={'errors': str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ShowSubscriptionViewSet(ListViewSet):
    """Отображает текущие подписки пользователя."""

    queryset = User.objects.all()
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            subscribers__user=user
        ).annotate(
            recipes_count=Count('recipes')
        )


class DownloadShoppingCart(views.APIView):
    """
    Обработка запроса на скачивание списка покупок.
    После обработки корзина очищается.
    """

    def get(self, request):
        user = request.user
        queryset = user.shopping_cart.select_related('recipe').all()
        message = get_header_message(queryset)
        total_list = get_total_list(queryset)

        with open('total_list.txt', 'w', encoding='utf-8') as f:
            f.write(f'{message}\n\n')
            for k, v in total_list.items():
                for unit, amount in v.items():
                    f.write(f'{k}: {amount} {unit}\n')

        user.shopping_cart.all().delete()
        return FileResponse(open('total_list.txt', 'rb'), as_attachment=True)
