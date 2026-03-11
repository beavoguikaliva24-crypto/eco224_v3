from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "contact", "email", "first_name", "last_name",
            "adress", "profession", "photo", "role", "permission",
            "is_active", "is_staff", "date_joined", "updated_at",
        ]
        read_only_fields = ["permission", "is_staff", "date_joined", "updated_at"]

