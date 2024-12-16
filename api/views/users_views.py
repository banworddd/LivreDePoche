from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.db.models import Avg
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from api.permissions import IsAuthenticatedOrReadOnly
from api.serializers.users_serializers import UserSerializer, LoginSerializer, ReadingListSerializer,  UserReviewSerializer, UserListSerializer, FriendsListSerializer
from users.models import CustomUser, ReadingList, BookReview, FriendsList
from api.utils import send_welcome_email

from drf_yasg.utils import swagger_auto_schema


class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer


class BookReviewsAndAverageRatingView(ListAPIView):
    serializer_class = UserReviewSerializer

    @swagger_auto_schema(operation_description='Возвращает набор отзывов, связанных с книгой по ее id')
    def get_queryset(self):
        book_id = self.kwargs.get('book_id')
        return BookReview.objects.filter(book_id=book_id)

    @swagger_auto_schema(operation_description='Возвращает список отзывов и средний рейтинг этих отзывов')
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        average_rating = queryset.aggregate(Avg('rating'))['rating__avg']
        return Response({
            'reviews': serializer.data,
            'average_rating': average_rating
        })


class UserRegistration(APIView):

    @swagger_auto_schema(operation_description='Создает пользователя в БД')
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

    @swagger_auto_schema(operation_description='Авторизирует пользователя с указанными данными')
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"status": "Login successful"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(operation_description='Получает данные профиля пользователя')
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description='Обновляет профиль пользователя.')
    def post(self, request, username):
        user = get_object_or_404(CustomUser, username=username)

        if user != request.user:
            return Response({'error': 'У вас нет прав на изменение этого профиля.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReadingListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # Используйте новый класс разрешений

    @swagger_auto_schema(operation_description='Получает списки чтения пользователя по username')
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        reading_list = ReadingList.objects.filter(user=user)
        serializer = ReadingListSerializer(reading_list, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description='Создает/правит записи в списках для чтения пользователя')
    def post(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        book_id = request.data.get('book')
        status_name = request.data.get('status')

        if not book_id or not status_name:
            return Response({"error": "Не указаны необходимые данные."}, status=status.HTTP_400_BAD_REQUEST)

        existing_entry = ReadingList.objects.filter(user=user, book_id=book_id).first()

        if existing_entry:
            existing_entry.status = status_name
            existing_entry.read_date = timezone.now().date() if status_name == 'completed' else None
            existing_entry.save()

            serializer = ReadingListSerializer(existing_entry)
            return Response(serializer.data, status=status.HTTP_200_OK)

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

    @swagger_auto_schema(operation_description='Удаляет запись из списков пользователя')
    def delete(self, request, username, reading_list_id):
        try:
            print(f"Попытка удалить запись для пользователя {username} и записи с ID {reading_list_id}")

            reading_list_entry = ReadingList.objects.get(id=reading_list_id, user__username=username)
            reading_list_entry.delete()
            print(f"Запись успешно удалена: {reading_list_entry}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReadingList.DoesNotExist:
            print(f"Запись не найдена для пользователя {username} и записи с ID {reading_list_id}")
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserBookReviewsView(APIView):
    @swagger_auto_schema(operation_description='Получает отзывы пользователя по его username')
    def get(self, request, username):
        reviews = BookReview.objects.filter(user__username=username)

        if reviews.exists():
            serializer = UserReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Отзывы не найдены."}, status=status.HTTP_404_NOT_FOUND)




