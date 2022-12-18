from django.db.models import Sum
from django.http import HttpResponse
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from core.messages import ERRORS
from .filters import IngredientFilter, RecipeFilter
from .mixins import CreateDeleteMixin
from .pagination import CustomPageNumberPagination
from .permissions import AdminOrAuthorEditOrReadOnly, AdminOrReadOnly
from recipes.models import (Favorite,
                            Ingredient,
                            IngredientInRecipe,
                            Recipe,
                            ShoppingCart,
                            Tag
                            )
from .serializers import (CustomUserSerializer,
                          IngredientSerializer,
                          RecipeCreateUpdateSerializer,
                          RecipeFavoriteCartSerializer,
                          RecipeGetSerializer,
                          SubscriptionsSerializer,
                          TagSerializer
                          )
from users.models import Follow, User
from .service import create_pdf_shopping_list

class RecipeViewSet(viewsets.ModelViewSet, CreateDeleteMixin):
    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer
    permission_classes = (AdminOrAuthorEditOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch',
                         'delete', 'options', 'headers'
                         ]

    def get_serializer_class(self):
        if self.action in ('favorite', 'shopping_cart'):
            serializer = RecipeFavoriteCartSerializer
        if self.action in ('create', 'delete', 'partial_update'):
            serializer = RecipeCreateUpdateSerializer
        if self.request.method in SAFE_METHODS:
            serializer = RecipeGetSerializer
        return serializer

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            response = {'detail': ERRORS['PUT_NOT_ALLOWED']}
            return Response(response,
                            status=status.HTTP_405_METHOD_NOT_ALLOWED
                            )
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        """Добавление/удаление рецептов в избранном."""
        return self.create_delete(
            request=request,
            model=Favorite,
            field='recipe',
            pk=pk
        )

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        """Добавление/удаление рецептов в корзину."""
        return self.create_delete(
            request=request,
            model=ShoppingCart,
            field='recipe',
            pk=pk
        )

    @action(detail=False)
    def download_shopping_cart(self, request):
        """Скачать список покупок."""
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return create_pdf_shopping_list(request)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотри тэги списком и по-отдельности."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    permission_classes = (AdminOrReadOnly,)
    pagination_class = None


class UserViewSet(DjoserUserViewSet, CreateDeleteMixin):
    queryset = User.objects.all()
    pagination_class = CustomPageNumberPagination
    permission_classes = (AdminOrAuthorEditOrReadOnly,)
    serializer_class = CustomUserSerializer

    def get_serializer_class(self):
        if self.action in ('subscribe', 'subscriptions'):
            return SubscriptionsSerializer
        return super().get_serializer_class()

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,)
            )
    def subscribe(self, request, id=None):
        """Добавление/удаление подписок пользователя."""
        return self.create_delete(
            request=request,
            model=Follow,
            field='author',
            pk=id
        )

    @action(detail=False,
            permission_classes=(IsAuthenticated,)
            )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(authors__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            many=True,
            instance=pages,
            context={'request': request}
            )
        return self.get_paginated_response(serializer.data)
