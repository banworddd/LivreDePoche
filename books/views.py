from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from books.models import Book, Author
from users.models import (
    ReadingList,
    CurrentlyReadingList,
    PlannedReadingList,
    BookReview
)

def books_view(request):
    """Отображает список книг."""
    books = Book.objects.all()
    return render(request, 'books/books.html', {'books': books})

def book_detail_view(request, book_id):
    """Отображает детальную информацию о книге."""
    book = get_object_or_404(Book, id=book_id)

    # Проверка наличия отзывов на книгу
    reviews = BookReview.objects.filter(book=book)

    # Проверка, если у пользователя есть книга в списках
    is_read = ReadingList.objects.filter(user=request.user, book=book).exists()
    is_reading = CurrentlyReadingList.objects.filter(user=request.user, book=book).exists()
    is_planned = PlannedReadingList.objects.filter(user=request.user, book=book).exists()

    # Получение существующего отзыва пользователя (если есть)
    existing_review = BookReview.objects.filter(user=request.user, book=book).first() if request.user.is_authenticated else None

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'read':
            ReadingList.objects.get_or_create(user=request.user, book=book)
            is_read = True  # Обновляем состояние
        elif action == 'reading':
            CurrentlyReadingList.objects.get_or_create(user=request.user, book=book)
            is_reading = True  # Обновляем состояние
        elif action == 'planned':
            PlannedReadingList.objects.get_or_create(user=request.user, book=book)
            is_planned = True  # Обновляем состояние
        elif action == 'add_review':
            rating = request.POST.get('rating')
            review_text = request.POST.get('review_text')

            # Преобразуем рейтинг в целое число
            try:
                rating = int(rating)
            except (ValueError, TypeError):
                rating = None  # В случае ошибки установка None

            if existing_review:
                # Обновляем существующий отзыв
                existing_review.rating = rating
                existing_review.review_text = review_text
                existing_review.review_date = timezone.now()
                existing_review.save()
            else:
                # Создаем новый отзыв
                BookReview.objects.create(
                    user=request.user,
                    book=book,
                    rating=rating,
                    review_text=review_text,
                    review_date=timezone.now()
                )

            # Обновляем или создаем запись в ReadingList
            if rating is not None:  # Проверка, чтобы избежать ошибок
                ReadingList.objects.update_or_create(
                    user=request.user,
                    book=book,
                    defaults={'rating': rating, 'read_date': timezone.now()}  # или другая логика
                )

            # После добавления перенаправляем на ту же страницу
            return redirect('book_detail', book_id=book.id)

    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'is_read': is_read,
        'is_reading': is_reading,
        'is_planned': is_planned,
        'existing_review': existing_review  # Передаем существующий отзыв
    })


@login_required
def add_review(request, book_id):
    """Добавляет или обновляет отзыв на книгу."""
    book = get_object_or_404(Book, id=book_id)

    # Получаем существующий отзыв, если он есть
    existing_review = BookReview.objects.filter(user=request.user, book=book).first()

    if request.method == 'POST':
        # Получаем рейтинг и текст отзыва из POST-запроса
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        # Преобразуем рейтинг в целое число
        try:
            rating = int(rating)
        except (ValueError, TypeError):
            rating = None  # В случае ошибки установка None

        if existing_review:
            # Обновляем существующий отзыв
            existing_review.rating = rating
            existing_review.review_text = review_text
            existing_review.review_date = timezone.now()
            existing_review.save()
        else:
            # Создаем новый отзыв
            BookReview.objects.create(
                user=request.user,
                book=book,
                rating=rating,
                review_text=review_text,
                review_date=timezone.now()
            )

        # Обновляем или создаем запись в ReadingList
        if rating is not None:  # Проверка, чтобы избежать ошибок
            ReadingList.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'rating': rating, 'read_date': timezone.now()}  # или другая логика
            )

        return redirect('book_detail', book_id=book.id)

    return redirect('book_detail', book_id=book.id)


def authors_view(request):
    """Отображает список авторов."""
    authors = Author.objects.all()
    return render(request, 'books/authors.html', {'authors': authors})

def author_detail_view(request, author_id):
    """Отображает детальную информацию об авторе."""
    author = get_object_or_404(Author, id=author_id)
    return render(request, 'books/author_detail.html', {'author': author})

def index(request):
    """Отображает главную страницу."""
    return render(request, 'books/index.html')
