from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q


User = get_user_model()

FIELD_NAMES = {
    'TITLE': 'Название',
    'PUB_DATE': 'Дата публикации',
    'COOKING_TIME': 'Время готовки',
}

class Ingredient(models.Model):
    """Модель сообщества (группы) содержит поля:
    - title - название сообщества;
    - количество - уникальный url адрес страницы сообщества;
    -  - единицы измерения;
    - функция __str__ переопределена и показывает название сообщества title.
    """
    # Все поля обязательны для заполнения.
    title = models.CharField(st.DEV_CON['GROUP_NAME'], max_length=200)
    slug = models.SlugField(st.DEV_CON['URL_NAME'], unique=True)
    description = models.TextField(st.DEV_CON['DESCRIPTION_NAME'])

    class Meta:
        verbose_name = st.DEV_CON['GROUP_NAME']
        verbose_name_plural = st.DEV_CON['GROUPS_NAME']

    def __str__(self):
        return(self.title)

class Recipe(models.Model):
    """Модель сообщения содержит поля:
    - author - автор (при удалении автора удаляются все рецепты);
    - title - название рецепта;
    - image - загружаемая картинка;
    - text - текст рецепта;
    - ingredients - ингридиенты;
    - tag - тэг;
    - cooking time - время приготовления в минутах;
    - pub_date - дата публикации рецепта.
    """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(FIELD_NAMES['TITLE'], max_length=200)
    image = models.ImageField(upload_to='recipes-images/')
    text = models.TextField()
    ingredients = models.ForeignKey(Ingredient, on_delete=models.PROTECT,
        related_name='recipes'
        )
    tags = models.ForeignKey(Ingredient, null=True, on_delete=models.SET_NULL,
        related_name='recipes'
        )
    cooking_time = models.PositiveSmallIntegerField(
        FIELD_NAMES['COOKING_TIME'], null=True
        )
    pub_date = models.DateTimeField(FIELD_NAMES['PUB_DATE'],
        auto_now_add=True
        )


class Tag(models.Model):
    """Модель тэга содержит поля:
    - title - название тэга;
    - color - цветовой HEX-код;
    - slug - уникальный url адрес страницы сообщества.
    """
    # Все поля обязательны для заполнения и уникальны.
    title = models.CharField(st.DEV_CON['GROUP_NAME'], max_length=200)
    slug = models.SlugField(st.DEV_CON['URL_NAME'], unique=True)
    description = models.TextField(st.DEV_CON['DESCRIPTION_NAME'])

    class Meta:
        verbose_name = st.DEV_CON['GROUP_NAME']
        verbose_name_plural = st.DEV_CON['GROUPS_NAME']

    def __str__(self):
        return(self.title)






class Follow(models.Model):
    """Модель подписки содержит поля:
    - user - подписчик;
    - author - автор интересующий подписчика.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name=st.DEV_CON['FOLLOWER_NAME']
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=st.DEV_CON['AUTHOR_NAME'],
        null=True
    )

    class Meta:
        ordering = ('-following',)
        verbose_name = st.DEV_CON['FOLLOW_NAME']
        verbose_name_plural = st.DEV_CON['FOLLOWS_NAME']
        constraints = [
            models.CheckConstraint(check=~Q(user=F('following')),
                                   name='disable_self-following'),
            models.UniqueConstraint(fields=('user', 'following'),
                                    name='unique_following')
        ]

    def __str__(self):
        return(f'{self.user} => {self.following}')