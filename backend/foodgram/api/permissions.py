from rest_framework.permissions import BasePermission, SAFE_METHODS


class RecipePermission(BasePermission):
    """
    Доступ на изменение/удаление только автору,
    создание - залогину, остальным только просмотр.
    Метод 'PUT' запрещен.
    """

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method != 'PUT':
            return (request.method in SAFE_METHODS
                    or request.user == obj.author)
