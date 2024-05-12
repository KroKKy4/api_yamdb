from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import (RegexValidator)

REGEX_LETTERS = RegexValidator(r'^[\w.@+-]+\Z', 'Поддерживаемые знаки.')
REGEX_ME = RegexValidator(r'[^m][^e]', 'Имя пользователя не может быть "me".')

REGEX_SLUG = RegexValidator(
    r'^[-a-zA-Z0-9_]+$', 'Недопустимые символы в slug.'
)


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )


def year_validator(value):
    if value > datetime.now().year:
        raise ValidationError(
            'Значение не может быть больше текущего.'
        )
