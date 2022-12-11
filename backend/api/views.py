from recipes.models import Favorite, Follow, Ingredient, IngredientInRecipe, Recipe, ShoppingCart, Tag, User
from rest_framework import filters, permissions, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from djoser.views import UserViewSet as DjoserUserViewSet

from .mixins import CreateListViewSet, CreateRetriveDeleteViewSet, CreateDeleteMixin
from .permissions import OnlyAuthorEditOrReadOnlyPremission
from .serializers import (
    FollowSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipeCreateUpdateSerializer,
    RecipeFavoriteCartSerializer,
    FavoriteSerializer,
    TagSerializer,
    CustomUserSerializer
    )
from .filters import RecipeFilter


class RecipeViewSet(viewsets.ModelViewSet, CreateDeleteMixin):
    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer
    # permission_classes = (IsAdminOrAuthorOrReadOnly,)
    pagination_class = PageNumberPagination
    filterset_class = RecipeFilter
    # http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'headers']

    def get_serializer_class(self):
        if (self.action == 'favorite' or
            self.action == 'shopping_cart'):
            serializer = RecipeFavoriteCartSerializer
        if (self.action == 'create' or
            self.action == 'delete' or
            self.action == 'patch'
            ):
            serializer = RecipeCreateUpdateSerializer
        if self.request.method in SAFE_METHODS:
            serializer = RecipeGetSerializer
        print('SERIALIZER = ', serializer)
        return serializer

    def perform_create(self, serializer):
        print('PERFORM CREATE')
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


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотри тэги списком и по-отдельности."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # permission_classes = (OnlyAuthorEditOrReadOnlyPremission,)


class FollowViewSet(CreateRetriveDeleteViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


class FavoriteViewSet(CreateListViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        # user_id = self.kwargs.get('user_id')
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


def download_shopping_cart(self, request):
        """Скачать список покупок."""
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_amount=Sum('amount')).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'ingredient_amount')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment;'
                                           'filename="Shoppingcart.csv"')
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        for item in list(ingredients):
            writer.writerow(item)
        return response


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    # permission_classes = (IsOwnerOrAdminOrReadOnly,)
    serializer_class = CustomUserSerializer

    # def get_serializer_class(self):
    #     if self.request.method is 'POST':
    #         return CustomUserCreateSerializer
    #     return super().get_serializer_class()

    @action(detail=True)     #, permission_classes=[IsAuthenticated]
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        data = {
            'user': user.id,
            'author': author.id,
        }
        serializer = FollowSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        subscribe = get_object_or_404(
            Follow, user=user, author=author
        )
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(detail=False, permission_classes=[IsAuthenticated])
    # def subscriptions(self, request):
    #     user = request.user
    #     queryset = Follow.objects.filter(user=user)
    #     pages = self.paginate_queryset(queryset)
    #     serializer = FollowerSerializer(
    #         pages,
    #         many=True,
    #         context={'request': request}
    #     )
    #     return self.get_paginated_response(serializer.data)