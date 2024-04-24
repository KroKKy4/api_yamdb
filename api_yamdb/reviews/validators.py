from datetime import datetime

from django.core.validators import (
    MaxValueValidator, MinValueValidator, RegexValidator
)

REGEX_LETTERS = RegexValidator(r'^[\w.@+-]+\Z', 'Поддерживаемые знаки.')
REGEX_ME = RegexValidator(r'[^m][^e]', 'Имя пользователя не может быть "me".')

REGEX_SLUG = RegexValidator(
    r'^[-a-zA-Z0-9_]+$', 'Недопустимые символы в slug.'
)
YEAR_VALIDATOR = (
    MinValueValidator(0, 'Год выпуска не может быть отрицательным числом.'),
    MaxValueValidator(
        datetime.now().year, 'Год выпуска не может быть больше текущего.'
    ),
)
