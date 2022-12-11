from django.urls import include, path

from rest_framework import routers

from . import views

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('recipes', views.RecipeViewSet, basename='resipes')
router_v1.register('tags', views.TagViewSet, basename='tags')
router_v1.register('ingredients', views.IngredientViewSet, basename='ingredients')
router_v1.register(r'users', views.UserViewSet, basename='user')

# router_v1.register(r'follow', views.FollowViewSet, basename='follow')
# router_v1.register(r'users/(?P<user_id>\d+)/favorites', views.FavoriteViewSet, basename='favorite')


urlpatterns = [
    path('', include(router_v1.urls)),
    # path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
