# FOODGRAM
Web-приложение позволяет постить и просматривать рецепты, формировать список покупок из ингридиентов в составе рецептов.

# YAMDB_FINAL
![Foodgram-project-react-app_workflow](https://github.com/Galenfea/foodgram-project-react/actions/workflows/foodgram-project-react.yml/badge.svg)

Предназначен для хранения и обмена рецепта, обеспечен CI:

- интерфейс реализован через REST API и web-страницы на react;
- есть регистрация и авторизация пользователей;
- добавление, редактирование и удаление рецептов;
- добавление рецептов в избранное и подписка на авторов;
- рецептам можно присваивать тэги, создаваемые администратором;
- разделение ролей на пользователей, модераторов и администраторов;
- модераторы и администраторы могут добавлять произведения, новые жанры и новые категории;
- при push в мастер ветку проводится тестирование на pep-8.

## Применяемые технологии:

- Python 3.10
- Django 4.1
- Django Rest Framework 3.13.1
- Docker 3.8
- Postgres 13.0
- Continuous Integration
- Continuous Deployment

## Как запустить проект:

**На Windows 10 корпоративной:**

***Если у вас не установлен Docker:***
- _откройте: Панель управления — Программы и компоненты — Включение и отключение компонентов Windows;_
- _активируйте пункт Hyper-V;_
- _перезагрузите систему._

_Установите Docker Desctop:_
[Docker Desctop для Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header)

***Если у вас уже установлен Docker***

_Клонируйте репозиторий:_
```
git clone https://github.com/Galenfea/foodgram-project-react.git
```

_Перейдите в репозиторий в командной строке:_
```
cd foodgram-project-react/infra
```

_Создайте файл .env:_
```
touch .env
```

_Скопируйте в него следующий шаблон и установить собственные значения:_
```
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=postgres 
POSTGRES_PASSWORD=postgres 
DB_HOST=db 
DB_PORT=5432
WEB_SECRET_KEY='your_secret_key' # ваш секретный ключ
WEB_ALLOWED_HOSTS==127.0.0.1 localhost <ваш ip сервер, если разворачиваете на сервере>
```

_Соберите необходимые образы:_
- для развёртывания на локальной машине:
```
docker-compose -f local-docker-compose.yml up -d
```
- для развёртывания на сервере:
```
docker-compose up -d
```

_Откройте админку на локальной машине:_
```
http://127.0.0.1/admin/
```

## Документация
После запуска автономного сервера документация API расположена по ардесу:

http://127.0.0.1/redoc/


## Адрес сервера для деплоя в рамках CI/CD:

http://158.160.26.27/api/docs/ - документация по API

http://158.160.26.27/admin/ - вход в админку


_Тестовый суперпользователь:_
```
email: admin@admin.com
password: admin
```


## Примеры запросов:

## Авторы:

- ***Отаров Александр*** -- вся внутренняя часть, REST API, упаковка в Docker, CI/CD; 
- Яндекс -- вэб-интерфейс сайта.


# Примеры POST запросов, для экономии времени:

## Создание пользователя:
```
{
"email": "cepesh@yandex.ru",
"username": "drakula",
"first_name": "Влад",
"last_name": "Цепеш",
"password": "123098QwePoi"
}
```

## Получение токена авторизации:
```
{
"password": "123098QwePoi",
"email": "cepesh@yandex.ru"
}
```

## Создание рецепта:
```
{
  "ingredients": [
    {
      "id": 1,
      "amount": 10
    },
    {
      "id": 2,
      "amount": 5
    },
    {
      "id": 3,
      "amount": 1
    }
  ],
  "tags": [1, 2],
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAeAB4AAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAYAB8DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD7Y+Hf/KOf4yf9gvW//TYtfknX62fDv/lHP8ZP+wXrf/psWvyTr+esh/5JnLP+vX6s/wBIvBP/AJGGef8AX+P/AKQgooorpP34/Wz4d/8AKOf4yf8AYL1v/wBNi1+SdFFc2Q/8kzln/Xr9WfgPgn/yMM8/6/x/9IQUUUV0n78f/9k=",
  "name": "Рецепт трёх ингредиентов",
  "text": "Смешайте ингридиенты 1 и 2 и 3 по технологии 1 к 1 к 3",
  "cooking_time": 15
}
```
