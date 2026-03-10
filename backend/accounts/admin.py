from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User

    ordering = ("contact",)
    list_display = ("id", "contact", "first_name", "last_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("contact", "first_name", "last_name", "email")

    # IMPORTANT: on ne met jamais "username" ici
    fieldsets = (
        (None, {"fields": ("contact", "password")}),
        (_("Informations personnelles"), {"fields": ("first_name", "last_name", "email", "adress", "profession", "photo")}),
        (_("Rôle & permission"), {"fields": ("role", "permission")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Dates importantes"), {"fields": ("last_login", "date_joined", "updated_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("contact", "first_name", "last_name", "email", "role", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    readonly_fields = ("permission", "last_login", "date_joined", "updated_at")