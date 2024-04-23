from django.core.validators import RegexValidator

REGEX_LETTERS = RegexValidator(r'^[\w.@+-]+\Z', 'Поддерживаемые знаки.')
REGEX_ME = RegexValidator(r'[^m][^e]', 'Имя пользователя не может быть "me".')
