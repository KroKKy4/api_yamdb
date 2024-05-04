# Generated by Django 3.2 on 2024-05-03 15:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_genre_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(unique=True, validators=[django.core.validators.RegexValidator('^[-a-zA-Z0-9_]+$', 'Недопустимые символы в slug.')], verbose_name='Slug'),
        ),
    ]