from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "contact", "email", "first_name", "last_name",
            "adress", "profession", "photo", "role", "permission",
            "is_active", "is_staff", "date_joined", "updated_at",
        ]
        read_only_fields = ["permission", "is_staff", "date_joined", "updated_at"]

class ChildSerializer(serializers.ModelSerializer):
    classe = serializers.CharField(source="current_class.name", default=None, allow_null=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "contact", "photo", "matricule", "classe"]