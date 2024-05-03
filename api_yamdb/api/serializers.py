from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import REGEX_LETTERS, REGEX_ME


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        validators=(REGEX_LETTERS, REGEX_ME)
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        title = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if Review.objects.filter(author=author, title__id=title).exists():
            raise serializers.ValidationError(
                'Нельзя повторно комментировать произведение!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',)

    class Meta:
        model = Comment
        exclude = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при GET-запросах."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj)
        rating = reviews.aggregate(Avg('score'))['score__avg']
        if rating:
            return rating
        return None


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title небезопасных запросах."""

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validate_genre(self, value):
        """Проверяет, что значение поля genre не None."""
        if not value:
            raise serializers.ValidationError(
                'This field is required.'
            )
        return value

    def to_representation(self, instance):
        """Сериализация ответа на POST-запрос."""
        serializer = TitleReadSerializer(instance)
        return serializer.data
