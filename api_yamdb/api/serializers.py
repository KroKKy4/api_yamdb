from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import REGEX_LETTERS, REGEX_ME, validate_username


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
    # прописываю отдельно поля сериализатора,
    # чтобы отменить действие UniqueValidator, который прописан в модели
    username = serializers.CharField(
        validators=[REGEX_LETTERS, REGEX_ME, validate_username],
        max_length=150
    )
    email = serializers.EmailField(validators=[], max_length=254)

    def validate(self, attrs):
        """Провожу проверку: username и email должны быть уникальными.

        Исключение, если пара username и email уже есть в бд.
        """
        username = attrs['username']
        email = attrs['email']

        user_username = User.objects.filter(username=username)
        user_email = User.objects.filter(email=email)

        if not user_username and not user_email:
            return attrs

        if not user_username and user_email:
            raise serializers.ValidationError(
                {'email': 'Этот email уже используется.'}
            )

        if user_username and not user_email:
            raise serializers.ValidationError(
                {'username': 'Этот username уже используется.'}
            )

        try:
            User.objects.get(username=username, email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                {'username': 'Этот username уже используется.',
                 'email': 'Этот email уже используется.'},
            )
        return attrs

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        user, created = User.objects.get_or_create(**validated_data)
        return user


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

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category',
        )

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj)
        rating = reviews.aggregate(Avg('score'))['score__avg']
        if rating:
            return rating
        return None


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при POST, PATCH, DELETE запросах."""

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        many=True, allow_null=False, allow_empty=False
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category',)

    def to_representation(self, instance):
        """Сериализация ответа на POST-запрос."""
        serializer = TitleReadSerializer(instance)
        return serializer.data
