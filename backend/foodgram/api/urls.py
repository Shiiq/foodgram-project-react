from django.urls import include, path
from rest_framework import routers

from .views import IngredientsViewSet, TagsViewSet, RecipesViewSet, MakeSubscriptionView, ShowSubscriptionViewSet, AddToFavorite

router = routers.DefaultRouter()
router.register('ingredients', IngredientsViewSet)
router.register('tags', TagsViewSet)
router.register('recipes', RecipesViewSet)
router.register(r'users\/subscriptions', ShowSubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:id>/subscribe/', MakeSubscriptionView.as_view()),
    path('recipes/<int:id>/favorite/', AddToFavorite.as_view())
]
