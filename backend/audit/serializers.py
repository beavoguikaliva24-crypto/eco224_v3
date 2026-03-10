from rest_framework import serializers
from .models import LogAction, Notification

class LogActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAction
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ["destinataire", "date_notification"]