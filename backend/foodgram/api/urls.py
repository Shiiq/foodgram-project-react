from django.urls import include, path
from rest_framework import routers

from .views import IngredientsViewSet, TagsViewSet, RecipesViewSet

router = routers.DefaultRouter()
router.register('ingredients', IngredientsViewSet)
router.register('tags', TagsViewSet)
router.register('recipes', RecipesViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]



# api/users/
# регистрация пользователя

# # Djoser создаст набор необходимых эндпоинтов.
# # базовые, для управления пользователями в Django:
# path('auth/', include('djoser.urls')),
# # JWT-эндпоинты, для управления JWT-токенами:
# path('auth/', include('djoser.urls.jwt')),