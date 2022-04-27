from django.urls import include, path
from rest_framework import routers

from recipes.models import Recipe, RecipeFavorite, ShoppingCart
from .views import (AddToFavOrShopCartCommonView, DownloadShoppingCart,
                    IngredientsViewSet, MakeSubscription, RecipesViewSet,
                    ShowSubscriptionViewSet, TagsViewSet)

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
             {'primary': RecipeFavorite, 'secondary': Recipe}),

        path('<int:id>/shopping_cart/', AddToFavOrShopCartCommonView.as_view(),
             {'primary': ShoppingCart, 'secondary': Recipe}),

        path('download_shopping_cart/', DownloadShoppingCart.as_view())
    ])),
    path('', include(router.urls)),
    path('', include('djoser.urls'))
]
