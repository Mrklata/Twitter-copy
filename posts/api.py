from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Post, PostRating
from posts.serializers import PostSerializer, PostRatingSerializer
from users.models import Profile


class CreatePostView(viewsets.ModelViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    model = Post
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(
        methods=['get'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_name='rating',
        url_path='rating'
    )
    def get_all_post_rates(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        data = {'rates': post.rates.values_list('rate', flat=True)}
        return Response(data)


class CreateWallView(viewsets.GenericViewSet, mixins.ListModelMixin):
    model = Post
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return Post.objects.filter(user__in=list(profile.friends_list.values_list('id', flat=True)))


class CreatePostRatingView(viewsets.ModelViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    model = PostRating
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostRatingSerializer

    def get_queryset(self):
        return PostRating.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = serializer.validated_data['post']
        user = self.request.user
        rate = serializer.validated_data['rate']
        post_rate = serializer.save(
            rate=rate,
            post=post,
            user=user
        )

        post.rates.add(post_rate)
        return Response(data={'status': 'ok', 'data': serializer.data})
