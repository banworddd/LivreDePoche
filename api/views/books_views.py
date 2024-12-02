from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthenticatedOrReadOnly
from api.serializers import  BookSerializer, BookReviewSerializer, BookReviewMarkSerializer
from users.models import  BookReview, BookReviewMark
from books.models import Book


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


class BookListView(APIView):
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


class BookReviewMarkAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        review_id = request.query_params.get('review')
        if review_id:
            marks = BookReviewMark.objects.filter(review_id=review_id)
        else:
            marks = BookReviewMark.objects.all()
        serializer = BookReviewMarkSerializer(marks, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = BookReviewMarkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, review_id):
        review = get_object_or_404(BookReview, id=review_id)
        mark = get_object_or_404(BookReviewMark, review=review, user=request.user)
        data = request.data.copy()
        serializer = BookReviewMarkSerializer(mark, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        review = get_object_or_404(BookReview, id=review_id)
        mark = get_object_or_404(BookReviewMark, review=review, user=request.user)
        mark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)