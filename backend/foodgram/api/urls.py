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
    path('auth/', include('djoser.urls.authtoken')),
]
