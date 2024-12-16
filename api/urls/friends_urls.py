from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from api.views.friends_views import (
    SendFriendRequestView,
    AcceptFriendRequestView,
    FriendsListView,
    DeleteFriendRequestView
)

app_name = 'friends'

urlpatterns = [
path('send_friend_request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('accept_friend_request/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friends_list/<str:username>/', FriendsListView.as_view(), name='friends-list'),
    path('delete_friend_request/<int:pk>/', DeleteFriendRequestView.as_view(), name='delete-friend-request'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)