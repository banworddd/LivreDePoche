from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from api.serializers.users_serializers import  FriendsListSerializer
from users.models import CustomUser, FriendsList


class FriendsListView(ListAPIView):
    serializer_class = FriendsListSerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        return FriendsList.objects.filter(user__username=username) | FriendsList.objects.filter(friend__username=username)


class SendFriendRequestView(CreateAPIView):
    queryset = FriendsList.objects.all()
    serializer_class = FriendsListSerializer

    def create(self, request, *args, **kwargs):
        friend_username = request.data.get('friend_username')
        if not friend_username:
            return Response({"detail": "Friend username is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            friend = CustomUser.objects.get(username=friend_username)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Friend not found."}, status=status.HTTP_404_NOT_FOUND)

        if FriendsList.objects.filter(user=request.user, friend=friend, status='waiting').exists():
            return Response({"detail": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)

        if FriendsList.objects.filter(user=request.user, friend=friend, status='accepted').exists():
            return Response({"detail": "You are already friends."}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendsList.objects.create(user=request.user, friend=friend, status='waiting')
        serializer = FriendsListSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AcceptFriendRequestView(UpdateAPIView):
    queryset = FriendsList.objects.all()
    serializer_class = FriendsListSerializer

    def update(self, request, *args, **kwargs):
        user = request.user
        friend_request_id = kwargs.get('pk')

        try:
            friend_request = FriendsList.objects.get(id=friend_request_id, friend=user, status='waiting')
        except FriendsList.DoesNotExist:
            return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

        friend_request.status = 'accepted'
        friend_request.save()

        serializer = FriendsListSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteFriendRequestView(DestroyAPIView):
    queryset = FriendsList.objects.all()
    serializer_class = FriendsListSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)