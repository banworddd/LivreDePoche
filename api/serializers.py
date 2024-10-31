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
    password = serializers.CharField(write_only=True)  # Указываем, что это поле только для записи
    avatar = serializers.ImageField(required=False, allow_null=True)  # Добавлено поле для аватара

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'password', 'avatar']  # Включите поле 'avatar'

    def create(self, validated_data):
        password = validated_data.pop('password')  # Удаляем пароль из validated_data
        user = CustomUser(**validated_data)  # Создаем экземпляр пользователя без пароля
        user.set_password(password)  # Устанавливаем пароль с хэшированием
        user.save()  # Сохраняем пользователя в базе данных
        return user

    def update(self, instance, validated_data):
        # Обновляем данные пользователя
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)

        # Обработка аватара, если он предоставлен
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']

        # Устанавливаем новый пароль, если он был предоставлен
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()  # Сохраняем изменения
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Попытка получить пользователя по электронной почте
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Пользователь с таким адресом электронной почты не существует."})

        # Проверка пароля
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль."})

        # Возвращаем валидированные данные
        return attrs  # Возвращаем атрибуты, которые были валидированы


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