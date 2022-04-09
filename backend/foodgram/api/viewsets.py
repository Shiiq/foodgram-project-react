from rest_framework import filters, mixins, viewsets


class CreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Вьюсет для POST/DELETE запросов.
    """
    pass
