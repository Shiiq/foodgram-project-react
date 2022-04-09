from django.urls import include, path
from rest_framework import routers

from .views import IngredientsViewSet, TagsViewSet, RecipesViewSet, MakeSubscription

router = routers.DefaultRouter()
router.register('ingredients', IngredientsViewSet)
router.register('tags', TagsViewSet)
router.register('recipes', RecipesViewSet)
# router.register('exp', ExpSerializer)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:id>/subscribe/', MakeSubscription.as_view())
]
