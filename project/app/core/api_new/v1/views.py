from app.core.api_new.v1.serializer import (UserMessageSerializer,
                                            UserTotalMessageSerializer)
from app.core.models import UserMessage
from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

User = get_user_model()


class UserTotalMessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserTotalMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserMessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserMessage.objects.filter(user=self.request.user, unread=True)[:10]
