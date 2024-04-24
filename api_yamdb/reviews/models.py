from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from .consts import (
    MAX_ROLE_LENGTH, NAME_MAX_LENGTH, SLUG_MAX_LENGTH, USERNAME_MAX_LENGTH
)
from .validators import REGEX_LETTERS, REGEX_ME, REGEX_SLUG, YEAR_VALIDATOR


class User(AbstractUser):
    username = models.CharField(
        'Никнейм', unique=True,
        max_length=USERNAME_MAX_LENGTH,
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
        'Имя пользователя', max_length=USERNAME_MAX_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия пользователя', max_length=USERNAME_MAX_LENGTH,
        blank=True,
    )


class Genre(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(
        'Slug',
        max_length=SLUG_MAX_LENGTH,
        validators=(REGEX_SLUG,),
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(
        'Slug',
        max_length=SLUG_MAX_LENGTH,
        validators=(REGEX_SLUG,),
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    year = models.IntegerField(
        'Год выпуска',
        validators=YEAR_VALIDATOR
    )
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Slug жанра',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Slug категории',
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Комментарий')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
