from django.db import models
from django.contrib.auth.models import AbstractUser

from .consts import (NAME_MAX_LENGTH, MAX_ROLE_LENGTH)
from .validators import (REGEX_LETTERS, REGEX_ME)


class User(AbstractUser):
    username = models.CharField(
        'Никнейм', unique=True,
        max_length=NAME_MAX_LENGTH,
        validators=(REGEX_LETTERS, REGEX_ME),
    )
    email = models.EmailField(
        'email', unique=True
    )
    role = models.CharField(
        'Роль', blank=True,
        default='user', max_length=MAX_ROLE_LENGTH,
    )
    bio = models.TextField(
        'Биография', blank=True,
    )
    first_name = models.CharField(
        'Имя пользователя', max_length=NAME_MAX_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия пользователя', max_length=NAME_MAX_LENGTH,
        blank=True,
    )


class Genre(models.Model):
    pass


class Category(models.Model):
    pass


class Title(models.Model):
    pass


class Review(models.Model):
    pass


class Comment(models.Model):
    pass
