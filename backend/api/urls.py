from django.urls import include, path

from rest_framework import routers

from . import views

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'recipes', views.RecipeViewSet, basename='resipes')
router_v1.register(r'tags', views.TagViewSet, basename='tags')
router_v1.register(r'ingredients', views.IngredientViewSet, basename='ingredients')
# router_v1.register(r'groups', views.GroupViewSet, basename='groups')
# router_v1.register(r'posts/(?P<post_id>\d+)/comments', views.CommentViewSet,
#                    basename='comments'
#                    )
router_v1.register(r'follow', views.FollowViewSet, basename='follow')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls.jwt')),
]
