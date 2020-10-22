from rest_framework import viewsets, mixins, permissions, status
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.models import User, FriendRequest, Profile
from users.serializers import UserSerializer, FriendRequestSerializer, FriendResponseSerializer, ProfileSerializer


class CreateUserView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    model = User
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return User.objects.all()


class CreateProfileView(viewsets.GenericViewSet, mixins.ListModelMixin):
    model = Profile
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()


class CreateFriendRequestView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    model = FriendRequest
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def perform_create(self, serializer):
        if serializer.data['to_user'] == self.request.user.id:
            return Response({'status': "can't invite yourself"})

        if FriendRequest.objects.filter(from_user=self.request.user, to_user=serializer.data['to_user']) or \
                FriendRequest.objects.filter(from_user=serializer.data['to_user'], to_user=self.request.user):

            return Response({'status': 'already exist'})
        else:
            return serializer.save(from_user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.data['to_user'] == self.request.user.id:
            return Response({'status': "can't invite yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=self.request.user, to_user=serializer.data['to_user']) or \
                FriendRequest.objects.filter(from_user=serializer.data['to_user'], to_user=self.request.user):

            return Response({'status': 'already exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.save(from_user=self.request.user)
            return Response(data, status=status.HTTP_201_CREATED)

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
        serializer = self.get_serializer(request.data)
        if friend_request.status == 'pending' and self.request.user == friend_request.to_user:

            if serializer.data['accepted'] == True:
                friend_request.status = 'accepted'
                giver = Profile.objects.get(user=friend_request.from_user)
                receiver = Profile.objects.get(user=friend_request.to_user)

                giver.friends_list.add(Profile.objects.get(user=friend_request.to_user))
                receiver.friends_list.add(Profile.objects.get(user=friend_request.from_user))

                friend_request.save()
            else:
                friend_request.status = 'declined'
                friend_request.delete()

        else:
            return Response({'status': 'already responded, or wrong user'})
        data = {"status": "ok", "data": FriendRequestSerializer(friend_request).data}
        return Response(data)
