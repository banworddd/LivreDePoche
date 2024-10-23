from django.urls import path
from . import views

urlpatterns = [
    path('books_list/', views.books_view, name='books'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('book/<int:book_id>/add_review/', views.add_review, name='add_review'),
    path('authors_list/', views.authors_view, name='authors'),
    path('author/<int:author_id>/', views.author_detail_view, name='author_detail'),
    path('', views.index, name='index'),
]
