from rest_framework import mixins, viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from djoser.views import UserViewSet

class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
    pass


class CustomUserViewSet(UserViewSet):
    pagination_class = LimitOffsetPagination
    pass
