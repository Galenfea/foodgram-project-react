from django.contrib import admin
from django.db.models import Count

from core.names import FIELDS
from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag, TagRecipe)


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
    list_display = ('pk', 'author', 'name',
        'in_favorites',
    )
    list_editable = ('author', 'name',)
    list_filter = ('author', 'name',)
    search_fields = ('author', 'name', 'tags', 'cooking_time',)
    empty_value_display = FIELDS['EMPTY']

    def in_favorites(self, obj):
        result = Favorite.objects.filter(recipe=obj).aggregate(Count('user'))
        return result["user__count"]


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