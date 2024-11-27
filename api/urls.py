from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import UserRegistration, UserLogin, ProfileView, ReadingListView, BookView, BookReviewView, \
    UserBookReviewsView, BookListView, UserListView, BookReviewMarkAPIView

app_name = 'api'
urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('reading_list/<str:username>/', ReadingListView.as_view(), name='reading_list'),
    path('reading_list/<str:username>/<int:reading_list_id>/', ReadingListView.as_view(), name='reading_list_delete'),
    path('book/<int:book_id>/', BookView.as_view(), name='book'),
    path('book/<int:book_id>/reviews/', BookReviewView.as_view(), name='book_reviews'),
    path('book/<int:book_id>/reviews/<int:review_id>/', BookReviewView.as_view(), name='book_review_detail'),
    path('user_reviews/<str:username>/', UserBookReviewsView.as_view(), name='user_reviews'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('user_list/', UserListView.as_view(), name='user-list'),
    path('bookreviewmarks/', BookReviewMarkAPIView.as_view(), name='bookreviewmark-list-create'),
    path('bookreviewmarks/<int:book_id>/', BookReviewMarkAPIView.as_view(), name='bookreviewmark-list-by-book'),
    path('bookreviewmarks/<int:review_id>/update/', BookReviewMarkAPIView.as_view(), name='bookreviewmark-update'),
    path('bookreviewmarks/<int:review_id>/delete/', BookReviewMarkAPIView.as_view(), name='bookreviewmark-delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)