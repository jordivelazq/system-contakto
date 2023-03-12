from app.core.models import UserMessage
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserTotalMessageSerializer(serializers.ModelSerializer):
    total_messages = serializers.SerializerMethodField()
    total_messages_unread = serializers.SerializerMethodField()
    total_messages_trash = serializers.SerializerMethodField()
    total_messages_read = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name',
                  'total_messages', 'total_messages_unread',
                  'total_messages_trash', 'total_messages_read']

    def get_total_messages(self, obj):
        return UserMessage.objects.filter(user=obj).count()

    def get_total_messages_unread(self, obj):
        return UserMessage.objects.filter(user=obj, unread=True).count()

    def get_total_messages_trash(self, obj):
        return UserMessage.objects.filter(user=obj, trash=True).count()

    def get_total_messages_read(self, obj):
        return UserMessage.objects.filter(user=obj, unread=False, trash=False).count()


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = ['id', 'user', 'title', 'message', 'link',
                  'unread', 'trash', 'created_at', 'last_modified_at']
