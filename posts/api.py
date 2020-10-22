from django.db.models import Q
from rest_framework import viewsets, mixins, permissions, status

from posts.models import Post
from posts.serializers import PostSerializer
from users.models import Profile


class CreatePostView(viewsets.ModelViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    model = Post
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CreateWallView(viewsets.GenericViewSet, mixins.ListModelMixin):
    model = Post
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return Post.objects.filter(author__in=list(profile.friends_list.values_list('id', flat=True)))
