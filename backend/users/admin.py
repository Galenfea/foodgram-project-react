from django.contrib import admin

from core.names import FIELDS
from .models import Follow, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Источник конфигурации модели User, позволяет:
    - отображать в админке первичный ключ, email, имя пользователя,
    фамилию, имя;
    - редактировать все поля, кроме первичного ключа;
    - проводить поиск и фильтровать по имени пользователя,
    имени, и фамилии;
    - выводить "-пусто-" в полях со значением None."""
    list_display = ('pk', 'email', 'username', 'is_active', 'first_name', 'last_name',)
    list_editable = ('email', 'username', 'is_active', 'first_name', 'last_name',)
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    list_filter = ('email', 'username',)
    empty_value_display = FIELDS['EMPTY']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Источник конфигурации модели Follow, регистрируемой в админке, позволяет:
    - отображать в админке первичный ключ, подписчика и
    автора, на которого происходит подписка;
    - редактировать все поля, кроме первичного ключа;
    - удалять подписку;
    - проводить поиск по авторам и подписчикам;
    - выводить "-пусто-" в полях со значением None."""
    list_display = ('pk', 'author', 'user',)
    list_editable = ('author', 'user',)
    search_fields = ('author', 'user',)
    empty_value_display = FIELDS['EMPTY']