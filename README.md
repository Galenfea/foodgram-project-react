
# ВНИМАНИЕ
В проекте присутствует библиотека django-cors-headers
Она активна для удобства проверки проекта на локальной машине.
На этапе создания инфраструктуры она будет удалена.

В данный момент проект использует sqlite. 
На инфраструктурном этапе субд будет заменена на PostgreSQL.

# FOODGRAM
Web-приложение позволяет постить и просматривать рецепты, формировать список покупок из ингридиентов в составе рецептов.

## Установка проекта

- Клонировать репозиторий:
```
git clone https://github.com/Galenfea/foodgram-project-react
```

- Перейти в папку проекта:
```
cd foodgram-project-react
```

- Создать виртуальное окружение:
```
python -m venv venv
```

- Активировать виртуальное окружение:
```
source venv/Scripts/activate
```

- Обновить установщик:
```
python -m pip install --upgrade pip
```

- Установить зависимости:
```
pip install -r requirements.txt
```

- Перейти в папку джанго сервера:
```
cd backend
```

- Выполнить миграции:
```
python manage.py migrate
```

- Создать суперпользователя:
```
python manage.py createsuperuser
```

## Документация к API
Доступна по следующему адресу после запуска сервера (адрес указан для dev-режима)
```
http://127.0.0.1/api/docs/
```


## Применяемые технологии:

- Python 3.7
- Django==4.1
- Pillow==9.2.0
- sorl-thumbnail==12.8.0

## Пример создания пользователя через POST запрос:
```
{
"email": "cepesh@yandex.ru",
"username": "drakula",
"first_name": "Влад",
"last_name": "Цепеш",
"password": "123098QwePoi"
}
```

## Пример получения токена авторизации через POST запрос:
```
{
"password": "123098QwePoi",
"email": "cepesh@yandex.ru"
}
```

## Пример создания рецепта через POST запрос:
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
