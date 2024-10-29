from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Указываем, что это поле только для записи

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'password']

    def create(self, validated_data):
        # Извлекаем пароль из валидации
        password = validated_data.pop('password')  # Удаляем пароль из validated_data
        user = CustomUser(**validated_data)  # Создаем экземпляр пользователя без пароля
        user.set_password(password)  # Устанавливаем пароль с хэшированием
        user.save()  # Сохраняем пользователя в базе данных
        return user


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