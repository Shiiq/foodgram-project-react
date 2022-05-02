from io import StringIO

from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, status, views, viewsets
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe, Tag
from users.models import Subscription, User

from .filters import IngredientSearchFilter, RecipeFilter
from .permissions import RecipePermission
from .serializers import (RecipesCreateSerializer, RecipesSerializer,
                          SubscribeSerializer)
from .simple_serializers import (IngredientsSerializer,
                                 RecipesShortInfoSerializer, TagsSerializer)
from .utils import get_header_message, get_total_list
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

    queryset = Recipe.objects.annotated()
    serializer_class = RecipesSerializer
    permission_classes = (RecipePermission, )
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        user = self.request.user
        return self.queryset.annotated(user).all()

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
        recipe = get_object_or_404(secondary, id=id)

        try:
            primary.objects.create(recipe=recipe, user=request.user)
        except IntegrityError as e:
            return Response(
                data={'errors': str(e.__context__)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RecipesShortInfoSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id, primary, secondary):
        recipe = get_object_or_404(secondary, id=id)

        try:
            primary.objects.get(recipe=recipe, user=request.user).delete()
        except primary.DoesNotExist:
            return Response(
                data={'errors': f'Такого нет в {primary._meta.verbose_name}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class MakeSubscription(views.APIView):
    """Обработка запросов на подписку/отписку."""

    def post(self, request, id):
        author = get_object_or_404(User, id=id)

        try:
            Subscription.objects.create(author=author, user=request.user)
        except IntegrityError as e:
            return Response(
                data={'errors': str(e.__context__)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SubscribeSerializer(
            User.objects.annotate(recipes_count=Count('recipes')).get(id=id),
            context={'request': request}
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)

        try:
            Subscription.objects.get(
                author=author,
                user=request.user
            ).delete()
        except Subscription.DoesNotExist:
            return Response(
                data={'errors': f'Вы не подписаны на {author}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


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
    Список группируется по ингредиентам в вызываемом методе "get_total_list".
    После обработки запроса и выдачи файла корзина очищается.
    """

    def get(self, request):
        user = request.user
        queryset = user.shopping_cart.select_related('recipe').all()
        message = get_header_message(queryset)
        total_list = get_total_list(queryset)

        f = StringIO()
        f.name = 'shopping-list.txt'
        f.write(f'{message}\n\n')
        for k, v in total_list.items():
            for unit, amount in v.items():
                f.write(f'{k}: {amount} {unit}\n')

        response = HttpResponse(f.getvalue(), content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={f.name}'
        user.shopping_cart.all().delete()

        return response
