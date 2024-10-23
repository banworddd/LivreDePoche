from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from books.models import Book, Author
from users.models import ReadingList, CurrentlyReadingList, PlannedReadingList, BookReview
def books_view(request):
    books = Book.objects.all()
    return render(request, 'books/books.html', {'books': books})

def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Проверка наличия отзывов на книгу
    reviews = BookReview.objects.filter(book=book)

    # Проверка, если у пользователя есть книга в списках
    is_read = ReadingList.objects.filter(user=request.user, book=book).exists()
    is_reading = CurrentlyReadingList.objects.filter(user=request.user, book=book).exists()
    is_planned = PlannedReadingList.objects.filter(user=request.user, book=book).exists()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'read':
            ReadingList.objects.get_or_create(user=request.user, book=book)
        elif action == 'reading':
            CurrentlyReadingList.objects.get_or_create(user=request.user, book=book)
        elif action == 'planned':
            PlannedReadingList.objects.get_or_create(user=request.user, book=book)

        # После добавления перенаправляем на ту же страницу
        return redirect('book_detail', book_id=book.id)

    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'is_read': is_read,
        'is_reading': is_reading,
        'is_planned': is_planned
    })



@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        # Создаем новый отзыв
        BookReview.objects.create(
            user=request.user,
            book=book,
            rating=rating,
            review_text=review_text,
            review_date=timezone.now()
        )
        return redirect('book_detail', book_id=book.id)

    return redirect('book_detail', book_id=book.id)

def authors_view(request):
    authors = Author.objects.all()
    return render(request, 'books/authors.html', {'authors': authors})

def author_detail_view(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, 'books/author_detail.html', {'author': author})
def index(request):
    return render(request, 'books/index.html')
# Create your views here.
