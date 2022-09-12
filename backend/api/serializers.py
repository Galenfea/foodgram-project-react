from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Follow, Ingredient, IngredientInRecipe, Recipe, Tag, User


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit',)
        model = Ingredient


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    class Meta:
        fields = ('ingredient', 'recipe', 'amount',)
        model = IngredientInRecipe


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)



class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    ingredients = IngredientSerializer(many=True)
    amount = IngredientInRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tag',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
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
