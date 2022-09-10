FIELDS = {
    # Recipe model
    'TITLE': 'Название',
    'PUB_DATE': 'Дата публикации',
    'COOKING_TIME': 'Время приготовления',
    # Tag model
    'TAG_NAME': 'Тэг',
    'URL_NAME': 'ссылка',
    # Follow model
    'AUTHOR_NAME': 'Автор',
    'FOLLOW_NAME': 'Подписчик',
    'FOLLOWS_NAME': 'Подписчики',
    'UNIT_NAME': 'Ед. измерения',
    'INGRIDIENT_NAME': 'Ингридиент',
    'INGRIDIENTS_NAME': 'Ингридиенты',
    'TAG_NAME': 'Тэг',
    'TAGS_NAME': 'Тэги',
    'COLOR_NAME': 'Цвет',
    'URL_NAME': 'Ссылка',

    # serialaizers fields
    'RECIPE_SERIALIZER': (
        'author',
        'title',
        'image',
        'text',
        'ingredients',
        'tag',
        'cooking_time',
        'pub_date',
    ),

    'INGREDIENT_SERIALIZER': (
        'title',
        'unit',
    ),

    'INGREDIENT_IN_RECIPE_SERIALIZER': (
        'ingredient',
        'recipe',
        'amount',
    ),

    'TAG_SERIALIZER': (
        'title',
        'color',
        'slug',
    ),
}
