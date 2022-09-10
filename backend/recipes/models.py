from django.db import models
from django.db.models import F, Q
from django.core.validators import MinValueValidator

from users.models import User
from field_names import FIELDS


class Ingredient(models.Model):
    """Модель ингридиента содержит поля:
    - title - название ингридиента;
    - unit - единица измерения;
    - функция __str__ переопределена и показывает название ингридиента title.
    """
    # Все поля обязательны для заполнения.
    name = models.CharField(FIELDS['GROUP_NAME'], max_length=200)
    measurement_unit = models.TextField(FIELDS['UNIT_NAME'], unique=True)

    class Meta:
        verbose_name = FIELDS['INGRIDIENT_NAME']
        verbose_name_plural = FIELDS['INGRIDIENTS_NAME']

    def __str__(self):
        return(self.name)


class Tag(models.Model):
    """Модель тэга содержит поля:
    - title - название тэга;
    - color - цветовой HEX-код;
    - slug - уникальный url адрес страницы тэга.
    """
    # Все поля обязательны для заполнения и уникальны.
    name = models.CharField(FIELDS['TAG_NAME'], max_length=200, unique=True)
    color = models.TextField(FIELDS['COLOR_NAME'], max_length=7, unique=True)
    slug = models.SlugField(FIELDS['URL_NAME'], unique=True)


    class Meta:
        verbose_name = FIELDS['TAG_NAME']
        verbose_name_plural = FIELDS['TAGS_NAME']

    def __str__(self):
        return(self.name)


class Recipe(models.Model):
    """Модель сообщения содержит поля:
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
        User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(FIELDS['TITLE'], max_length=200)
    image = models.ImageField(upload_to='recipes-images/')
    text = models.TextField()
    ingredients = models.ManyToManyField(FIELDS['INGRIDIENTS_NAME'],
        Ingredient,
        through='IngredientInRecipe',
        through_fields=('recipe', 'ingredient')
        )
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    cooking_time = models.PositiveSmallIntegerField(
        FIELDS['COOKING_TIME'], 
        validators=(MinValueValidator(1),)
    )
    pub_date = models.DateTimeField(FIELDS['PUB_DATE'],
        auto_now_add=True
    )


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),)
    )

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
    - author - автор интересующий подписчика.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name=FIELDS['FOLLOWER_NAME']
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=FIELDS['AUTHOR_NAME'],
        null=True
    )

    class Meta:
        ordering = ('-following',)
        verbose_name = FIELDS['FOLLOW_NAME']
        verbose_name_plural = FIELDS['FOLLOWS_NAME']
        constraints = [
            models.CheckConstraint(check=~Q(user=F('following')),
                                   name='disable_self-following'),
            models.UniqueConstraint(fields=('user', 'following'),
                                    name='unique_following')
        ]

    def __str__(self):
        return(f'{self.user} => {self.following}')





