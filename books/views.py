from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from books.models import Book, Author
from users.models import ReadingList, BookReview

def books_view(request):
    """Отображает список книг."""
    books = Book.objects.all()
    return render(request, 'books/books.html', {'books': books})

def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Получаем список отзывов для книги
    reviews = BookReview.objects.filter(book=book)

    # Проверяем, аутентифицирован ли пользователь
    if request.user.is_authenticated:
        # Проверяем, оставил ли текущий пользователь отзыв
        user_reviewed = reviews.filter(user=request.user).exists()
    else:
        user_reviewed = False

    # Передаем переменные в шаблон
    context = {
        'book': book,
        'reviews': reviews,
        'user_reviewed': user_reviewed,
    }
    return render(request, 'books/book_detail.html', context)

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
