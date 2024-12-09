from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from api.views.users_views import (
    UserRegistration,
    UserLogin,
    ProfileView,
    ReadingListView,
    UserBookReviewsView,
    UserListView,
    BookReviewsAndAverageRatingView,
    SendFriendRequestView,
    AcceptFriendRequestView,
    FriendsListView,
    DeleteFriendRequestView
)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('reading_list/<str:username>/', ReadingListView.as_view(), name='reading_list'),
    path('reading_list/<str:username>/<int:reading_list_id>/', ReadingListView.as_view(), name='reading_list_delete'),
    path('user_reviews/<str:username>/', UserBookReviewsView.as_view(), name='user_reviews'),
    path('user_list/', UserListView.as_view(), name='user-list'),
    path('rating_reviews/<int:book_id>/',BookReviewsAndAverageRatingView.as_view(), name='rating_reviews'),
    path('send_friend_request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('accept_friend_request/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friends_list/<str:username>/', FriendsListView.as_view(), name='friends-list'),
    path('delete_friend_request/<int:pk>/', DeleteFriendRequestView.as_view(), name='delete-friend-request'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)