from pathlib import Path
from django.db import migrations
from django.conf import settings
from json import loads

INITIAL_TAGS = [
    {'color': '#FFA300', 'name': 'Завтрак', 'slug': 'breakfast'},
    {'color': '#04B300', 'name': 'Обед', 'slug': 'lunch'},
    {'color': '#FF0075', 'name': 'Ужин', 'slug': 'dinner'},
]


def read_ingredients():
    DATA_ROOT = Path(Path(settings.BASE_DIR).parent, 'data/ingredients.json')
    f = open(DATA_ROOT, 'r', encoding='utf-8')
    ingredients = f.read()
    f.close()
    return loads(ingredients)


def add_data(apps, schema_editor, model, array):
    Model = apps.get_model('recipes', model)
    for instance in array:
        new_instance = Model(**instance)
        new_instance.save()


def remove_data(apps, schema_editor, model, array):
    Model = apps.get_model('recipes', model)
    for instance in array:
        Model.objects.get(name=instance['name']).delete


def add_ingredients_and_tags(apps, schema_editor):
    add_data(
        apps=apps, schema_editor=schema_editor,
        model='Ingredient', array=read_ingredients()
    )
    add_data(
        apps=apps, schema_editor=schema_editor,
        model='Tag', array=INITIAL_TAGS
        )


def remove_ingredients_and_tags(apps, schema_editor):
    remove_data(
        apps=apps, schema_editor=schema_editor,
        model='Ingredient', array=read_ingredients()
    )
    remove_data(
        apps=apps, schema_editor=schema_editor,
        model='Tag', array=INITIAL_TAGS
        )


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_ingredients_and_tags,
            remove_ingredients_and_tags
        ),
    ]
