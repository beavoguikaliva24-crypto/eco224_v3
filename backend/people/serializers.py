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
    contact = serializers.CharField(source="user.contact", read_only=True, default="")
    photo = serializers.ImageField(source="user.photo", read_only=True)
    first_name = serializers.CharField(source="prenom1", read_only=True)
    last_name = serializers.CharField(source="nom", read_only=True)
    classe = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "contact",
            "photo",
            "matricule",
            "classe",
            "date_naissance",
            "lieu_naissance",
            "genre",
        ]

    def get_classe(self, obj):
        # si ton modèle classe existe ailleurs, adapte ici
        return None