from django.urls import include, path
from rest_framework import routers

from .views import (AddToFavorite, AddToShoppingCart, DownloadShoppingCart,
                    IngredientsViewSet, MakeSubscription, RecipesViewSet,
                    ShowSubscriptionViewSet, TagsViewSet, AddToFavOrShopCartCommonView)

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'recipes', RecipesViewSet)
router.register(r'users/subscriptions', ShowSubscriptionViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:id>/subscribe/', MakeSubscription.as_view()),
    path('recipes/', include([

        path('<int:id>/favorite/', AddToFavOrShopCartCommonView.as_view(),
             {'primary': {'model': 'RecipeFavorite', 'app': 'recipes'},
              'secondary': {'model': 'Recipe', 'app': 'recipes'}}),

        path('<int:id>/shopping_cart/', AddToFavOrShopCartCommonView.as_view(),
             {'primary': {'model': 'ShoppingCart', 'app': 'recipes'},
              'secondary': {'model': 'Recipe', 'app': 'recipes'}}),

        path('download_shopping_cart/', DownloadShoppingCart.as_view())
    ])),
    path('', include(router.urls)),
    path('', include('djoser.urls'))
]
