from rest_framework import filters, mixins, viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from .pagination import CustomPagination


class ReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """Обработка запросов к ингрeдиентам"""
    permission_classes = (permissions.AllowAny, )
    pass


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pagination_class = LimitOffsetPagination
    pass
