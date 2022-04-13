from django.urls import include, path
from rest_framework import routers

from .views import (IngredientsViewSet, TagsViewSet, RecipesViewSet, MakeSubscription,
                    AddToFavorite, AddToShoppingCart, DownloadShoppingCart, ShowSubscriptionViewSet)

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'recipes', RecipesViewSet)
router.register(r'users/subscriptions', ShowSubscriptionViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:id>/subscribe/', MakeSubscription.as_view()),
    path('recipes/', include([
        path('<int:id>/favorite/', AddToFavorite.as_view()),
        path('<int:id>/shopping_cart/', AddToShoppingCart.as_view()),
        path('download_shopping_cart/', DownloadShoppingCart.as_view())
    ])),
    path('', include(router.urls)),
    path('', include('djoser.urls'))
]
