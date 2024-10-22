from django.shortcuts import render
from .models import Book, Author

def books_view(request):
    books = Book.objects.all()
    return render(request, 'books/books.html', {'books': books})

def authors_view(request):
    authors = Author.objects.all()
    return render(request, 'books/authors.html', {'authors': authors})

def index(request):
    return render(request, 'books/index.html')
# Create your views here.
