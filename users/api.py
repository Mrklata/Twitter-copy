from rest_framework import viewsets, mixins, permissions
from django.db.models import Q
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
    serializer_class = FriendResponseSerializer, FriendRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        requests = FriendRequest.objects.filter(to_user=self.request.user)
        return requests

    def perform_create(self, serializer):
        pass
