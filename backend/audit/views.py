from rest_framework import viewsets, permissions, mixins
from .models import LogAction, Notification
from .serializers import LogActionSerializer, NotificationSerializer

class LogActionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = LogAction.objects.all()
    serializer_class = LogActionSerializer

class MesNotificationsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(destinataire=self.request.user)

    def perform_create(self, serializer):
        serializer.save(destinataire=self.request.user)

class AuditViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.request.user.role != 'DEV':
            return [permissions.DenyAll()] # Seul le DEV peut passer
        return [permissions.IsAuthenticated()]