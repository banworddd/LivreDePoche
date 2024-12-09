from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthenticatedOrReadOnly
from api.serializers.books_serializers import  BookSerializer, BookReviewSerializer, ReviewLikeSerializer, AuthorSerializer
from users.models import  BookReview, ReviewLike
from books.models import Book, Author

from drf_yasg.utils import swagger_auto_schema


class BookView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = 'book_id'


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookAuthorListView(ListAPIView):
    serializer_class = BookSerializer

    @swagger_auto_schema(operation_description='Получает список книг автора по его id')
    def get_queryset(self):
        queryset = Book.objects.all()
        author_id = self.request.query_params.get('author_id')
        queryset = queryset.filter(authors__id=author_id)
        return queryset


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


class ReviewLikeAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_description='Возвращает либо конкретный лайк по его like_id, либо все лайки для данного отзыва по его review_id ')
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

    @swagger_auto_schema(operation_description='Создает лайк на отзыв, если он не существует у пользователя')
    def post(self, request, review_id):
        review = BookReview.objects.get(id=review_id)
        like, created = ReviewLike.objects.get_or_create(user=request.user, review=review)
        if created:
            serializer = ReviewLikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Like already exists."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description='Удаляет существующий у пользователя лайк')
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
            author = get_object_or_404(Author, id=author_id)
            serializer = AuthorSerializer(author)
        else:
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


