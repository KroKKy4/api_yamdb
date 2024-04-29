import csv
import os

from django.core.management.base import BaseCommand

from api_yamdb.settings import CSV_FILES_DIR
from reviews.models import Category, Comment, Genre, Review, Title, User


CSV_FILE_NAMES_MODELS = {
    'users.csv': User,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'review.csv': Review,
    'comments.csv': Comment
}

FIELDS_MODELS = {
    'author': User,
    'category': Category
}


def loader(csv_file, model):
    csv_path = os.path.join(CSV_FILES_DIR, csv_file)
    try:
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                for key, value in row.items():
                    if key in FIELDS_MODELS:
                        row[key] = FIELDS_MODELS[key].objects.get(pk=value)
                model(**row).save()
        print(f'Данные из файла {csv_file} успешно загружены.')
    except FileNotFoundError:
        print(f'Файл {csv_file} не найден.')


def loader_genre_title(title_model, genre_model, csv_file):
    csv_path = os.path.join(CSV_FILES_DIR, csv_file)
    try:
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = title_model.objects.get(pk=row['title_id'])
                genre = genre_model.objects.get(pk=row['genre_id'])
                title.genre.add(genre)
        print(f'Данные из файла {csv_file} успешно загружены.')
    except FileNotFoundError:
        print(f'Файл {csv_file} не найден.')


class Command(BaseCommand):
    help = 'Uploading csv files to the database'

    def handle(self, *args, **options):
        for csv_file, model in CSV_FILE_NAMES_MODELS.items():
            loader(csv_file, model)
        loader_genre_title(Title, Genre, 'genre_title.csv')
