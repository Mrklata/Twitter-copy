from rest_framework import viewsets, mixins, permissions
from django.db.models import Q
from users.models import User, FriendRequest
from users.serializers import UserSerializer, FriendRequestSerializer


class CreateUserView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    model = User
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return User.objects.all()


class CreateFriendRequestView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    model = FriendRequest
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        user = self.request.user

        return FriendRequest.objects.filter(Q(from_user=user) | Q(to_user=user))
