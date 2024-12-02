from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from api.views.books_views import  BookView, BookReviewView, BookListView, BookReviewMarkAPIView, AuthorDetailView

app_name = 'books'
urlpatterns = [
    path('book/<int:book_id>/', BookView.as_view(), name='book'),
    path('book/<int:book_id>/reviews/', BookReviewView.as_view(), name='book_reviews'),
    path('book/<int:book_id>/reviews/<int:review_id>/', BookReviewView.as_view(), name='book_review_detail'),
    path('books_list/', BookListView.as_view(), name='book-list'),
    path('bookreviewmarks/', BookReviewMarkAPIView.as_view(), name='bookreviewmark-list-create'),
    path('bookreviewmarks/<int:book_id>/', BookReviewMarkAPIView.as_view(), name='bookreviewmark-list-by-book'),
    path('bookreviewmarks/<int:review_id>/update/', BookReviewMarkAPIView.as_view(), name='bookreviewmark-update'),
    path('bookreviewmarks/<int:review_id>/delete/', BookReviewMarkAPIView.as_view(), name='bookreviewmark-delete'),
    re_path(r'^author/(?:(?P<author_id>\d+)/)?$', AuthorDetailView.as_view(), name='author-detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)