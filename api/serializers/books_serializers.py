from rest_framework import serializers

from users.models import BookReview, BookReviewMark
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


class BookReviewMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReviewMark
        fields = '__all__'

    def validate(self, data):
        review = data.get('review')
        user = data.get('user')
        if BookReviewMark.objects.filter(review=review, user=user).exists():
            raise serializers.ValidationError("You have already marked this review.")
        return data

    def create(self, validated_data):
        return BookReviewMark.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.mark = validated_data.get('mark', instance.mark)
        instance.save()
        return instance