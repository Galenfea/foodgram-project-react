from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.db import transaction


from recipes.models import (Favorite, Follow, Ingredient, IngredientInRecipe, Recipe, 
                            ShoppingCart, Tag, TagRecipe)
from users.models import User

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name',)

class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed',)
        model = User

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit',)
        model = Ingredient


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
#        validators = [
#            UniqueTogetherValidator(
#                queryset=IngredientInRecipe.objects.all(),
#                fields=['ingredient', 'recipe']
#            )
#        ]


class IngredientInRecipeSerializerCreate(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount', 'recipe')

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class TagRecipeSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    tag = serializers.PrimaryKeyRelatedField(
        queryset=TagRecipe.objects.all(),
        source='tag'
    )
    class Meta:
        model = TagRecipe
        fields = ('recipe', 'tag',)


class RecipeGetSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True
    )
    ingredients = IngredientInRecipeSerializer(
        source='ingredientinrecipe_set',
        many=True,
        read_only=True,
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True
    )
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    # TODO В будущем реализовать через аннотацию,
    # чтобы не лезть по два раза в базу на каждом рецепте.
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def _filter_current_user_value(self, obj, model):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return model.objects.filter(user=user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        return self._filter_current_user_value(obj=obj, model=Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self._filter_current_user_value(obj=obj, model=ShoppingCart)


class RecipeFavoriteCartSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        use_url=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(required=False)
    ingredients = IngredientInRecipeSerializerCreate(
        many=True
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )


    class Meta:
        model = Recipe
        fields = (
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    @transaction.atomic
    def create(self, validated_data):
        print('CREATE BEGIN')
        # получаем список словарей с ингредиентами и их количеством
        ingredients = validated_data.pop('ingredients')
        print(f'INGREDIENTS: {ingredients}')
        tags = validated_data.pop('tags')
        print(f'TAGS: {tags}')
        print(f'VALIDATED_DATA: {validated_data}')
        recipe = Recipe.objects.create(**validated_data)
        # итерируемый объект
        test_generator = [
            print(f'СЛОВАРЬ: {ingredient}') for ingredient in ingredients
        ]
        bulk_ingredients = [
            IngredientInRecipe(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        print(f'bulk {bulk_ingredients}')
        print(f'tags {tags}')
        recipe.tags.set(tags)
        IngredientInRecipe.objects.bulk_create(bulk_ingredients)
        print('CREATE END')
        return recipe


    def update(self, instance, validated_data):
        '''Перезапиши все поля модели рецепта.'''
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        if ingredients is not None:
            instance.ingredients.clear()
        if tags is not None:
            instance.tags.set(tags)

        bulk_ingredients= [
            IngredientInRecipe(
                recipe=instance,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]            
        IngredientInRecipe.objects.bulk_create(bulk_ingredients)
        return super().update(instance, validated_data)


class SubscriptionsSerializer(CustomUserSerializer):
    recipes = RecipeFavoriteCartSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name', 
            'is_subscribed',
            'recipes', 
            'recipes_count',)
        model = User

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
