from rest_framework import mixins, permissions, viewsets


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class RetrieveListModelViewSet(mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny, )
