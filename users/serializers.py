from rest_framework import serializers

from users.models import User, FriendRequest, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        write_only_fields = ('password',)
        read_only_fields = ('id', 'admin', 'staff', 'active', 'last_login')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'
        write_only_fields = ('to_user',)
        read_only_fields = ('from_user', 'timestamp', 'status', 'last_login')

        def create(self, validated_data):
            friend_request = FriendRequest.objects.create(
                to_user=validated_data['to_user']
            )
            return friend_request


class FriendResponseSerializer(serializers.Serializer):
    accepted = serializers.BooleanField(default=False)
