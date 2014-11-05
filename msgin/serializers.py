from rest_framework import serializers
from msgin.models import Message, User


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.Field(source='sender.username')

    class Meta:
        model = Message
        fields = (
            'sender',
            'user_receiver',
            'group_receiver',
            'message_content',
            'send_time',
            'status',
            'created_at')


class UserSerializer(serializers.ModelSerializer):
    sent_messages = serializers.PrimaryKeyRelatedField(
        many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'sent_messages',
        )


# class GroupSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Group
#         fields = (
#         )
