from django.urls import path
from . import views

urlpatterns = [
    path('books_list', views.books_view, name='books'),
    path('authors_list/', views.authors_view, name='authors'),
    path('', views.index, name = '')
]