from colorfield.fields import ColorField
from django.db import models
from django.db.models import F, Q
from django.core.validators import MinValueValidator
from users.models import User
from core.names import FIELDS


class Ingredient(models.Model):
    """Модель ингридиента содержит поля:
    - title - название ингридиента;
    - measurement_unit - единица измерения;
    - функция __str__ переопределена и показывает название ингридиента title.
    """
    name = models.CharField(
        FIELDS['INGRIDIENT_NAME'],
        max_length=200
    )
    measurement_unit = models.CharField(
        FIELDS['UNIT_NAME'],
        max_length=200
    )

    class Meta:
        ordering = ('name',)
        verbose_name = FIELDS['INGRIDIENT_NAME']
        verbose_name_plural = FIELDS['INGRIDIENTS_NAME']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель тэга содержит поля:
    - name - название тэга;
    - color - цветовой HEX-код;
    - slug - уникальный url адрес страницы тэга.
    """
    name = models.CharField(
        FIELDS['TAG_NAME'],
        max_length=200,
        unique=True
    )
    color = ColorField(
        FIELDS['COLOR_NAME'],
        default=FIELDS['COLOR_DEFAULT'],
        max_length=7, unique=True
    )
    slug = models.SlugField(
        FIELDS['URL_NAME'],
        unique=True
    )


    class Meta:
        ordering = ('name',)
        verbose_name = FIELDS['TAG_NAME']
        verbose_name_plural = FIELDS['TAGS_NAME']

    def __str__(self):
        return(self.name)


class Recipe(models.Model):
    """Модель рецепта содержит поля:
    - author - автор (при удалении автора удаляются все рецепты);
    - title - название рецепта;
    - image - загружаемая картинка;
    - text - текст рецепта;
    - ingredients - ингридиенты;
    - tag - тэг;
    - cooking_time - время приготовления в минутах;
    - pub_date - дата публикации рецепта.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        FIELDS['TITLE'], 
        max_length=200
    )
    image = models.ImageField(
        verbose_name= FIELDS['IMAGE'],
        upload_to='recipes-img/'
    )
    text = models.TextField(
        FIELDS['RECIPES_TEXT']
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name=FIELDS['INGRIDIENTS_NAME'],
        through='IngredientInRecipe',
        through_fields=('recipe', 'ingredient')
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=FIELDS['TAGS_NAME'],
        through='TagRecipe'
    )
    cooking_time = models.PositiveSmallIntegerField(
        FIELDS['COOKING_TIME'], 
        validators=(MinValueValidator(1),)
    )
    pub_date = models.DateTimeField(
        FIELDS['PUB_DATE'],
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = FIELDS['RECIPE_NAME']
        verbose_name_plural = FIELDS['RECIPES_NAME']
    
    def __str__(self):
        return self.name[:15]


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),)
    )

    class Meta:
        verbose_name = FIELDS['INGREDIENT_IN_RECIPE_NAME']
        verbose_name_plural = FIELDS['INGREDIENT_IN_RECIPE_NAMES']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            )
        ]

    def __str__(self):
        return (f'{self.recipe} {self.ingredient}'
                f' {self.amount} {self.ingredient.measurement_unit}')


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}' 


class Follow(models.Model):
    """Модель подписки содержит поля:
    - user - подписчик;
    - author - автор интересующий подписчика;
    - функция __str__ переопределена.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name=FIELDS['FOLLOWER_NAME']
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name=FIELDS['AUTHOR_NAME'],
        null=True
    )

    class Meta:
        ordering = ('-author',)
        verbose_name = FIELDS['FOLLOWER_NAME']
        verbose_name_plural = FIELDS['FOLLOWERS_NAME']
        constraints = [
            models.CheckConstraint(check=~Q(user=F('author')),
                                   name='disable_self-folowing'),
            models.UniqueConstraint(fields=('user', 'author'),
                                    name='unique_folowing')
        ]

    def __str__(self):
        return(f'{self.user} => {self.author}')


class Favorite(models.Model):
    '''Модель избранных рецептов содержит поля:
    - user - пользователь добавивший в избранное рецепт;
    - recipe - избранный рецепт;
    - функция __str__ переопределена.
    '''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fans',
        verbose_name=FIELDS['FAN_NAME']
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=FIELDS['RECIPE_NAME'],
    )

    class Meta:
        verbose_name = FIELDS['FAVORITES_NAME']
        verbose_name_plural = FIELDS['FAVORITES_NAME']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        return(f'{self.user.username} => {self.recipe.name[:15]}')


class ShoppingCart(models.Model):
    '''Модель списка покупок содержит поля:
    - user - пользователь добавивший рецепт в список покупок;
    - recipe - рецепт в списке покупок;
    - функция __str__ переопределена.
    '''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyers',
        verbose_name=FIELDS['BUYER']
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name=FIELDS['RECIPE_NAME'],
    )

    class Meta:
        verbose_name = FIELDS['CART_NAME']
        verbose_name_plural = FIELDS['CARTS_NAME']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_shoppingcart')
        ]

    def __str__(self):
        return(f'Список покупок {self.user} => {self.recipe.name}')