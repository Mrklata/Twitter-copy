from rest_framework import serializers

from posts.models import Post, PostRating


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'id', 'rates')


class PostRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostRating
        fields = '__all__'
        read_only_fields = ('user', 'id')

    def create(self, validated_data):
        post_rate = PostRating.objects.create(
            rate=validated_data['rate'],
            post=validated_data['post'],
            user=validated_data['user']
        )
        return post_rate
