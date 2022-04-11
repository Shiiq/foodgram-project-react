from django.urls import include, path
from rest_framework import routers

from .views import IngredientsViewSet, TagsViewSet, RecipesViewSet, MakeSubscription, ShowSubscriptionViewSet, AddToFavorite

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientsViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'recipes', RecipesViewSet)
router.register(r'users/subscriptions', ShowSubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:id>/subscribe/', MakeSubscription.as_view()),
    path('recipes/<int:id>/favorite/', AddToFavorite.as_view()),
    # path('recipes/<int:id>/shopping_cart/') (get-скачать, post-добавить, del-удалить)
]
