# from constants.names import FIELDS
from core.names import FIELDS
from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientInRecipe,
                     Recipe, ShoppingCart, Tag, TagRecipe)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Источник конфигурации модели Ingredient, позволяет:
    - отображать в админке первичный ключ, название и единицы измерения
    для каждого ингредиента;
    - редактировать все поля, кроме первичного ключа;
    - проводить поиск и фильтровать по названию ингредиента;
    - выводить "-пусто-" в полях со значением None."""
    list_display = ('pk', 'name', 'measurement_unit',)
    list_editable = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = FIELDS['EMPTY']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Источник конфигурации модели Tag, позволяет:
    - отображать в админке первичный ключ, название, цвет и slug тэга;
    - редактировать название и цвет тэга;
    - проводить поиск по названию тэга;
    - выводить "-пусто-" в полях со значением None."""
    list_display = ('pk', 'name', 'color', 'slug',)
    list_editable = ('name', 'color',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = FIELDS['EMPTY']


class IngredientInRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through


class TagRecipeInline(admin.TabularInline):
    model = Recipe.tags.through

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Источник конфигурации модели Recipe, позволяет:
    - отображать в админке первичный ключ, автора, название, картинку, 
    текст, время приготовления и дату публикации рецепта;
    - редактировать всё, кроме первичного ключа;
    - проводить поиск по автору, названию, тэгам, времени приготовления;
    - выводить "-пусто-" в полях со значением None."""
    inlines = (IngredientInRecipeInline, TagRecipeInline,)
    exclude = ('ingredients', 'tags',)
    list_display = ('pk', 'author', 'name', 'image', 'text', 'cooking_time', 'pub_date',
                    )
    list_editable = ('author', 'name', 'text', 'cooking_time',
                     )
    search_fields = ('author', 'name', 'tags', 'cooking_time',)
    list_filter = ('name',)
    empty_value_display = FIELDS['EMPTY']


# @admin.register(IngredientInRecipe)
# class IngredientInRecipeAdmin(admin.ModelAdmin):
#     """Источник конфигурации модели IngredientInRecipe, позволяет:
#     - отображать в админке первичный ключ, ингредиент, рецепт  и количество
#     ингредиента в рецепте;
#     - редактировать все поля, кроме первичного ключа;
#     - проводить поиск по игредиенту и руцепту;
#     - выводить "-пусто-" в полях со значением None."""
#     list_display = ('pk', 'ingredient', 'recipe', 'amount',)
#     list_editable = ('ingredient', 'recipe', 'amount',)
#     search_fields = ('ingredient', 'recipe',)
#     list_filter = ('ingredient', 'recipe',)
#     empty_value_display = FIELDS['EMPTY']




# @admin.register(TagRecipe)
# class TagRecipe(admin.ModelAdmin):
#     """Источник конфигурации модели TagRecipe, позволяет:
#     - отображать в админке первичный ключ, id тэга и рецепта;
#     - редактировать рецепт и тэг;
#     - проводить поиск по тэгу;
#     - выводить "-пусто-" в полях со значением None."""
#     list_display = ('pk', 'tag', 'recipe',)
#     list_editable = ('tag', 'recipe',)
#     search_fields = ('tag', 'recipe',)
#     list_filter = ('tag', 'recipe',)
#     empty_value_display = FIELDS['EMPTY']




@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Источник конфигурации модели Follow, регистрируемой в админке, позволяет:
    - отображать в админке первичный ключ, подписчика и
    автора, на которого происходит подписка;
    - удалять подписку;
    - проводить поиск по авторам и подписчикам;
    - выводить "-пусто-" в полях со значением None."""
    list_display = ('pk', 'author', 'user',)
    search_fields = ('author', 'user',)
    empty_value_display = FIELDS['EMPTY']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Источник конфигурации модели Favorites, регистрируемой в админке, позволяет:
    - отображать в админке первичный ключ, подписчика и
    автора, на которого происходит подписка;
    - удалять подписку;
    - проводить поиск по авторам и подписчикам;
    - выводить "-пусто-" в полях со значением None."""
    list_display = ('pk', 'user', 'recipe',)
    search_fields = ('user', 'recipe',)
    empty_value_display = FIELDS['EMPTY']


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Источник конфигурации модели ShoppingCart, регистрируемой в админке, позволяет:
    - отображать в админке первичный ключ, покупателя и рецепты
    для списка покупок;
    - удалять рецепт;
    - проводить поиск по покупателям и рецептам;
    - выводить "-пусто-" в полях со значением None."""
    list_display = ('pk', 'user', 'recipe',)
    search_fields = ('user', 'recipe',)
    empty_value_display = FIELDS['EMPTY']