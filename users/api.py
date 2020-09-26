from rest_framework import viewsets, mixins, permissions
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.models import User, FriendRequest
from users.serializers import UserSerializer, FriendRequestSerializer, FriendResponseSerializer


class CreateUserView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    model = User
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return User.objects.all()


class CreateFriendRequestView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    model = FriendRequest
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def perform_create(self, serializer):
        return serializer.save(from_user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(Q(from_user=user) | Q(to_user=user))


class CreateFriendResponseView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = FriendResponseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = FriendRequest.objects.all()

    def get_queryset(self):
        user = self.request.user
        response = FriendRequest.objects.filter(to_user=user)
        return response

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_path='invitation_response',
        url_name='invitation_response'
    )
    def response_to_friend_request(self, request, pk=None):
        friend_request = get_object_or_404(FriendRequest, pk=pk)
        print(request.data)

        serializer = self.get_serializer(request.data)
        if friend_request.status == 'pending':

            if serializer.data['accepted'] == True:
                friend_request.status = 'accepted'
                friend_request.save()
            else:
                friend_request.status = 'declined'
                friend_request.delete()

        else:
            return Response({'status': 'already responded'})
        data = {"status": "ok", "data": FriendRequestSerializer(friend_request).data}
        return Response(data)
