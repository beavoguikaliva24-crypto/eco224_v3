from rest_framework import serializers
from .models import Student, Teacher, Parent


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"


class ParentChildSerializer(serializers.ModelSerializer):
    # Données "enfant" lisibles par le frontend
    full_name = serializers.CharField(source="Student.full_name", read_only=True)
    matricule = serializers.CharField(source="Student.matricule", read_only=True)
    genre = serializers.CharField(source="Student.genre", read_only=True)
    date_naissance = serializers.CharField(source="Student.date_naissance", read_only=True)
    lieu_naissance = serializers.CharField(source="Student.lieu_naissance", read_only=True)
    is_active = serializers.BooleanField(source="Student.is_active", read_only=True)
    photo = serializers.ImageField(source="Student.photo", read_only=True)
    id = serializers.IntegerField(source="Student.id", read_only=True)

    # Données du compte user lié à l'élève (si présent)
    contact = serializers.CharField(source="User.contact", read_only=True, default="")
    email = serializers.EmailField(source="User.email", read_only=True, default="")
    user_photo = serializers.ImageField(source="User.photo", read_only=True)

    # Parent lié (utile debug/affichage)
    parent_id = serializers.IntegerField(source="Parent.id", read_only=True)
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "matricule",
            "full_name",
            "genre",
            "photo",
            "user_photo",
            "contact",
            "email",
            "date_naissance",
            "lieu_naissance",
            "is_active",
            "parent_id",
            "parent_name",
        ]

    def get_parent_name(self, obj):
        if obj.parents and obj.parents.user:
            return obj.parents.user.get_full_name()
        return ""