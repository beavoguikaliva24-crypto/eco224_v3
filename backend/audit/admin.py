from django.contrib import admin
from .models import LogAction, Notification

@admin.register(LogAction)
class LogActionAdmin(admin.ModelAdmin):
    list_display = ("id", "date_action", "utilisateur", "action", "table_nom", "adresse_ip")
    list_filter = ("action", "date_action")
    search_fields = ("table_nom", "description", "utilisateur__contact")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "date_notification", "destinataire", "titre", "is_read")
    list_filter = ("is_read", "date_notification")
    search_fields = ("titre", "message", "destinataire__contact")