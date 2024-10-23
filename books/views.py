from django.shortcuts import render, get_object_or_404
from .models import Book, Author

def books_view(request):
    books = Book.objects.all()
    return render(request, 'books/books.html', {'books': books})

def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})
def authors_view(request):
    authors = Author.objects.all()
    return render(request, 'books/authors.html', {'authors': authors})

def author_detail_view(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, 'books/author_detail.html', {'author': author})
def index(request):
    return render(request, 'books/index.html')
# Create your views here.
