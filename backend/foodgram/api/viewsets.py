from djoser.views import UserViewSet
from rest_framework import mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
    pass


class CustomUserViewSet(UserViewSet):
    pagination_class = LimitOffsetPagination
    pass


class RetrieveListModelViewSet(mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny, )
    pass
