from rest_framework import serializers

from users.models import CustomUser,ReadingList, BookReview
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


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'password', 'avatar']

    @staticmethod
    def validate_email(value):
        email = value.lower()
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Этот email уже используется.")
        return email

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()  # Преобразуем email в нижний регистр
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'email' in validated_data:
            validated_data['email'] = validated_data['email'].lower()  # Преобразуем email в нижний регистр
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Приводим email к нижнему регистру
        email = attrs.get('email').lower()
        password = attrs.get('password')

        # Пытаемся найти пользователя
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Пользователь с таким адресом электронной почты не существует."}
            )

        # Проверяем пароль
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль."})

        # Сохраняем пользователя для дальнейшего использования
        attrs['user'] = user
        return attrs


class ReadingListSerializer(serializers.ModelSerializer):
    # Указываем PrimaryKeyRelatedField, чтобы сериализатор ожидал только ID книги
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = ReadingList
        fields = ['id', 'status', 'read_date', 'user', 'book']
        read_only_fields = ['id', 'rating']

    def validate(self, data):
        user = data.get('user')
        book = data.get('book') if 'book' in data else self.instance.book if self.instance else None
        status = data.get('status') if 'status' in data else self.instance.status if self.instance else None

        # Проверка на уникальность только для новой записи (без статуса обновления)
        if not self.instance and ReadingList.objects.filter(user=user, book=book).exists():
            raise serializers.ValidationError(
                "A record with this book already exists for this user."
            )

        # Если статус 'completed', проверяем наличие даты прочтения
        if status == 'completed' and not data.get('read_date'):
            raise serializers.ValidationError(
                "Read date is required when the status is 'completed'."
            )

        return data

class BookReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Возвращает имя пользователя

    class Meta:
        model = BookReview
        fields = ['id', 'user', 'rating', 'review_text', 'review_date']
        read_only_fields = ['id', 'user', 'review_date']

class UserReviewSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title')  # Добавляем название книги в сериализатор

    class Meta:
        model = BookReview
        fields = ['id', 'user', 'book_title', 'rating', 'review_text', 'review_date','book_id']  # Поля, которые должны быть включены в сериализатор

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'bio', 'avatar']