from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import UserRegistration, UserLogin, ProfileView, ReadingListView, BookView

app_name = 'api'
urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('reading_list/<str:username>/', ReadingListView.as_view(), name='reading_list'),
    path('reading_list/<str:username>/<int:reading_list_id>/', ReadingListView.as_view(), name='reading_list_delete'),
    path('book/<int:book_id>/', BookView.as_view(), name='book'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)