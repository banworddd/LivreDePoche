from rest_framework import serializers

from users.models import BookReview, ReviewLike
from books.models import Book, Author, Genre


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)  # Вложенные данные авторов
    genre = GenreSerializer(many=True, read_only=True)     # Вложенные данные жанров

    class Meta:
        model = Book
        fields = '__all__'


class BookReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Возвращает имя пользователя

    class Meta:
        model = BookReview
        fields = ['id', 'user', 'rating', 'review_text', 'review_date']
        read_only_fields = ['id', 'user', 'review_date']

class ReviewLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Возвращает имя пользователя

    class Meta:
        model = ReviewLike
        fields = ['id', 'user', 'review', 'like_date']
        read_only_fields = ['id', 'user', 'like_date']


