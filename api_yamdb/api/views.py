from rest_framework import viewsets

from .permissions import (AdminOnly, AuthorAdminModeratorOrReadOnly)
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from reviews.models import (User, Category, Genre, Title, Review, Comment)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
