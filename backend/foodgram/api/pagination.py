from rest_framework.pagination import PageNumberPagination


class IngredientsPagination(PageNumberPagination):
    page_size = 15
