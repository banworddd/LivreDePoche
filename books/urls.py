from django.urls import path
from . import views

urlpatterns = [
    path('books_list', views.books_view, name='books'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),  # Маршрут для детальной страницы книги
    path('authors_list/', views.authors_view, name='authors'),
    path('author/<int:author_id>/', views.author_detail_view, name='author_detail'),
    path('', views.index, name = '')
]