# cats/permissions.py
from rest_framework import permissions


"""Что могут делать неавторизованные пользователи

Создать аккаунт.
Просматривать рецепты на главной.
Просматривать отдельные страницы рецептов.
Просматривать страницы пользователей.
Фильтровать рецепты по тегам.


Что могут делать авторизованные пользователи

Входить в систему под своим логином и паролем.
Выходить из системы (разлогиниваться).
Менять свой пароль.
Создавать/редактировать/удалять собственные рецепты
Просматривать рецепты на главной.
Просматривать страницы пользователей.
Просматривать отдельные страницы рецептов.
Фильтровать рецепты по тегам.
Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингридиентов для рецептов из списка покупок.
Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.


Что может делать администратор

Администратор обладает всеми правами авторизованного пользователя.
Плюс к этому он может:
изменять пароль любого пользователя,
создавать/блокировать/удалять аккаунты пользователей,
редактировать/удалять любые рецепты,
добавлять/удалять/редактировать ингредиенты.
добавлять/удалять/редактировать теги.
Все эти функции нужно реализовать в стандартной админ-панели Django."""


class AdminOrAuthorEditOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS)
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_superuser)


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS)
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)