from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Follow, Ingredient, IngredientInRecipe, Recipe, Tag, TagRecipe, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name',)
        model = User


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

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True
    )
    
    ingredients = IngredientInRecipeSerializer(
        source='ingredientinrecipe_set',
        many=True,
        read_only=True,
    )
    tags = TagSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
#            'is_favorited',
#            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )





class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    user = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
    )

    class Meta:
        fields = ('id', 'user', 'author',)
        model = Follow

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate(self, data):
        if data['following'] == self.context['request'].user:
            raise serializers.ValidationError('Нельзя подписаться на себя!')
        return data
