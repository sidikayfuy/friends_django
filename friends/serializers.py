from rest_framework import serializers
from .models import CustomUser, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username')


class UserWithFriendsSerializer(serializers.ModelSerializer):
    friends = UserSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'friends')


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(many=False, read_only=True)
    recipient = UserSerializer(many=False, read_only=True)
    type = serializers.SerializerMethodField('request_type')

    class Meta:
        model = FriendRequest
        fields = ('id', 'sender', 'recipient', 'type')

    def request_type(self, obj):
        user = self.context.get("user")
        if user == obj.sender:
            return 'outgoing'
        else:
            return 'incoming'

