from recipes.models import Ingredient, Tag, Recipe, RecipeIngredients, RecipeTags
from users.models import User, Subscription
from django.shortcuts import get_object_or_404
from rest_framework import filters, views, viewsets, status
from .serializers import IngredientsSerializer, TagsSerializer, RecipesSerializer
from .pagination import IngredientsPagination


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Обработка запросов к ингрeдиентам"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = IngredientsPagination
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['^name', ]


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer


# class MakeSubscriptionViewSet(CreateDeleteViewSet):
#     queryset = Subscription.objects.all()
#     serializer_class = MakeSubscriptionSerializer

from rest_framework.response import Response


class MakeSubscription(views.APIView):
    """Обработка запросов на подписку/отписку."""
    def post(self, request, id):
        author = get_object_or_404(User, id=id)
        Subscription.objects.create(
            author=author,
            subscriber=request.user
        )
        # serializer = TagsSerializer()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        Subscription.objects.filter(
            author=author,
            subscriber=request.user
        ).delete()
        # serializer = TagsSerializer()
        return Response(status=status.HTTP_204_NO_CONTENT)