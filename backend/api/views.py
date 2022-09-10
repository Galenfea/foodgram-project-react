from django.shortcuts import get_object_or_404
from recipes.models import Follow, Ingredient, IngredientInRecipe, Recipe, Tag
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .mixins import CreateListViewSet
from .permissions import OnlyAuthorEditOrReadOnlyPremission
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # permission_classes = (OnlyAuthorEditOrReadOnlyPremission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (OnlyAuthorEditOrReadOnlyPremission,)
    pagination_class = LimitOffsetPagination


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # permission_classes = (OnlyAuthorEditOrReadOnlyPremission,)
    pagination_class = LimitOffsetPagination


# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     permission_classes = (OnlyAuthorEditOrReadOnlyPremission,)
#     pagination_class = LimitOffsetPagination
# 
#     def perform_create(self, serializer):
#         post_id = self.kwargs.get('post_id')
#         post = Post.objects.get(id=post_id)
#         serializer.save(author=self.request.user, post=post)
# 
#     def get_queryset(self):
#         post_id = self.kwargs.get('post_id')
#         post = get_object_or_404(Post, id=post_id)
#         return Comment.objects.filter(post=post)


class FollowViewSet(CreateListViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()
