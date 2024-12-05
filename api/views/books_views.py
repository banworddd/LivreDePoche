from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthenticatedOrReadOnly
from api.serializers.books_serializers import  BookSerializer, BookReviewSerializer, ReviewLikeSerializer, AuthorSerializer
from users.models import  BookReview, ReviewLike
from books.models import Book, Author

from drf_yasg.utils import swagger_auto_schema


class BookView(APIView):
    @swagger_auto_schema(operation_description='Получает запись из модели Book')
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)


class BookReviewView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description='Получает список отзывов на книгу по ее id')
    def get(self, request, book_id):
        reviews = BookReview.objects.filter(book=book_id)
        serializer = BookReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description='Добавляет отзыв на книгу по ее id')
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description='Редактирование отзыва на книгу по ее id и review id')
    def put(self, request, book_id, review_id):
        review = get_object_or_404(BookReview, id=review_id, book_id=book_id, user=request.user)
        serializer = BookReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description='Удаление отзыва на книгу по ее id и review id')
    def delete(self, request, book_id, review_id):
        review = get_object_or_404(BookReview, id=review_id, book_id=book_id, user=request.user)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookListView(APIView):

    @swagger_auto_schema(operation_description='Получаем список книг из модели Books, с возможностью фильтрации ')
    def get(self, request):
        # Получаем параметры фильтрации из запроса
        author_name = request.GET.get('author', None)
        genre_name = request.GET.get('genre', None)
        search_query = request.GET.get('search', None)

        books = Book.objects.all()

        # Фильтрация по автору
        if author_name:
            author_name = author_name.strip()  # Убираем лишние пробелы
            books = books.filter(authors__name__icontains=author_name)

        # Фильтрация по жанру
        if genre_name:
            genre_name = genre_name.strip()  # Убираем лишние пробелы
            books = books.filter(genre__name__icontains=genre_name)

        # Фильтрация по поисковому запросу
        if search_query:
            search_query = search_query.strip()  # Убираем лишние пробелы
            query = Q()
            for keyword in search_query.split():  # Разделяем поисковую строку на слова
                query |= Q(title__icontains=keyword) | Q(authors__name__icontains=keyword) | Q(genre__name__icontains=keyword)
            books = books.filter(query)

        # Применяем distinct, чтобы избежать повторений
        books = books.distinct()

        # Сериализация данных и возвращение ответа
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class ReviewLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, review_id, like_id=None):
        if like_id:
            try:
                like = ReviewLike.objects.get(id=like_id, review_id=review_id)
                serializer = ReviewLikeSerializer(like)
                return Response(serializer.data)
            except ReviewLike.DoesNotExist:
                return Response({"detail": "Like not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            likes = ReviewLike.objects.filter(review_id=review_id)
            serializer = ReviewLikeSerializer(likes, many=True)
            return Response(serializer.data)

    def post(self, request, review_id):
        review = BookReview.objects.get(id=review_id)
        like, created = ReviewLike.objects.get_or_create(user=request.user, review=review)
        if created:
            serializer = ReviewLikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Like already exists."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id, like_id):
        try:
            like = ReviewLike.objects.get(id=like_id, review_id=review_id, user=request.user)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReviewLike.DoesNotExist:
            return Response({"detail": "Like not found."}, status=status.HTTP_404_NOT_FOUND)

class AuthorDetailView(APIView):

    @swagger_auto_schema(operation_description='Получает информацию об авторе по его id или список всех авторов, если id не передан')
    def get(self, request, author_id=None):
        if author_id:
            # Получаем автора по ID или возвращаем 404 ошибку, если автор не найден
            author = get_object_or_404(Author, id=author_id)
            # Сериализуем данные автора
            serializer = AuthorSerializer(author)
        else:
            # Получаем всех авторов
            authors = Author.objects.all()
            # Сериализуем данные всех авторов
            serializer = AuthorSerializer(authors, many=True)

        # Возвращаем сериализованные данные в ответе
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookAuthorListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        author_id = self.request.query_params.get('author_id')
        if author_id is not None:
            queryset = queryset.filter(authors__id=author_id)
        return queryset