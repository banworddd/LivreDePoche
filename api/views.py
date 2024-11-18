from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import MultiPartParser, FormParser

from .permissions import IsAuthenticatedOrReadOnly
from .serializers import UserSerializer, LoginSerializer, ReadingListSerializer, BookSerializer, BookReviewSerializer
from users.models import CustomUser, ReadingList, BookReview
from books.models import Book


class UserRegistration(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                login(request, user)
                send_welcome_email(user)
                return Response({"status": "User created", "id": user.id}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error in UserRegistration API:", e)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogin(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = CustomUser.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)  # Убедитесь, что пользователь логинится
                    return Response({"status": "Login successful"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Неверный пароль."}, status=status.HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                return Response({"error": "Пользователь с таким адресом электронной почты не существует."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # Используйте новый класс разрешений
    parser_classes = [MultiPartParser, FormParser]  # Поддержка загрузки файлов

    def get(self, request, username):
        """Получает данные профиля пользователя."""
        user = get_object_or_404(CustomUser, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, username):
        """Обновляет профиль пользователя."""
        user = get_object_or_404(CustomUser, username=username)

        # Проверяем, является ли текущий пользователь владельцем профиля
        if user != request.user:
            return Response({'error': 'У вас нет прав на изменение этого профиля.'}, status=status.HTTP_403_FORBIDDEN)

        # Обновляем данные пользователя, включая аватар и биографию
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Сохраняем изменения
            return Response(serializer.data)  # Возвращаем обновлённые данные
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReadingListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # Используйте новый класс разрешений

    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        reading_list = ReadingList.objects.filter(user=user)
        serializer = ReadingListSerializer(reading_list, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        book_id = request.data.get('book')
        status_name = request.data.get('status')

        if not book_id or not status_name:
            return Response({"error": "Не указаны необходимые данные."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка на наличие существующей записи для данной книги
        existing_entry = ReadingList.objects.filter(user=user, book_id=book_id).first()

        if existing_entry:
            # Обновляем статус, если запись уже существует
            existing_entry.status = status_name
            existing_entry.read_date = timezone.now().date() if status_name == 'completed' else None
            existing_entry.save()

            serializer = ReadingListSerializer(existing_entry)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Если записи нет, создаем новую
        serializer = ReadingListSerializer(data={
            'user': user.id,
            'book': book_id,
            'status': status_name,
            'read_date': timezone.now().date() if status_name == 'completed' else None
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, reading_list_id):
        try:
            print(f"Попытка удалить запись для пользователя {username} и записи с ID {reading_list_id}")

            # Получаем запись списка чтения по ID записи и пользователю
            reading_list_entry = ReadingList.objects.get(id=reading_list_id, user__username=username)
            reading_list_entry.delete()
            print(f"Запись успешно удалена: {reading_list_entry}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReadingList.DoesNotExist:
            print(f"Запись не найдена для пользователя {username} и записи с ID {reading_list_id}")
            return Response(status=status.HTTP_404_NOT_FOUND)


class BookView(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

class BookReviewView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, book_id):
        """Получение списка отзывов на книгу."""
        book = get_object_or_404(Book, id=book_id)
        reviews = BookReview.objects.filter(book=book)
        serializer = BookReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, book_id):
        """Добавление нового отзыва."""
        book = get_object_or_404(Book, id=book_id)
        serializer = BookReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, book_id, review_id):
        """Редактирование отзыва пользователя на книгу."""
        review = get_object_or_404(BookReview, id=review_id, book_id=book_id, user=request.user)
        serializer = BookReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id, review_id):
        """Удаление отзыва пользователя на книгу."""
        review = get_object_or_404(BookReview, id=review_id, book_id=book_id, user=request.user)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserReviewsView(APIView):
    """
    API для работы с отзывами на книги, написанными конкретным пользователем.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, username):
        """Получение списка отзывов, написанных пользователем."""
        user = get_object_or_404(CustomUser, username=username)
        reviews = BookReview.objects.filter(user=user)
        serializer = BookReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        """Добавление нового отзыва текущим пользователем."""
        # Убедимся, что пользователь пишет от своего имени
        if request.user.username != username:
            return Response(
                {"detail": "Вы не можете добавлять отзывы от имени другого пользователя."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = BookReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, username, review_id):
        """Редактирование отзыва текущего пользователя."""
        # Убедимся, что пользователь редактирует свой отзыв
        if request.user.username != username:
            return Response(
                {"detail": "Вы не можете редактировать отзывы другого пользователя."},
                status=status.HTTP_403_FORBIDDEN
            )
        review = get_object_or_404(BookReview, id=review_id, user=request.user)
        serializer = BookReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, review_id):
        """Удаление отзыва текущего пользователя."""
        # Убедимся, что пользователь удаляет свой отзыв
        if request.user.username != username:
            return Response(
                {"detail": "Вы не можете удалять отзывы другого пользователя."},
                status=status.HTTP_403_FORBIDDEN
            )
        review = get_object_or_404(BookReview, id=review_id, user=request.user)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def send_welcome_email(user):
    subject = 'Добро пожаловать в наш сервис!'
    message = f'Привет, {user.username}! Спасибо за регистрацию.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, email_from, recipient_list)