# FOODGRAM
![Foodgram-app_workflow](https://github.com/Galenfea/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
Web-приложение позволяет постить свои рецепты, просматривать чужие, формировать список покупок из ингридиентов в составе рецептов.


## Применяемые технологии:

- Python 3.7
- asgiref==3.5.2
- Django==4.1
- Pillow==9.2.0
- sorl-thumbnail==12.8.0
- sqlparse==0.4.2
- tzdata==2022.2


### Этапы разработки
- создание джанго проекта foodgram;
- перенос содержимого папки проекта foodgram в папку backend;
- создание приложения recipes и его регистрация в settings.py;
- установка графической библиотеки Pillow и приложения sorl-thumbnail;
- создание наброска модели Рецепта
- добавление в foodgram/urls.py адресов для авторизации
- добавление промежуточных моделей "многие ко многим" для ингрилиентов и тэгов
- формирование большинства сериализаторов и view классов 