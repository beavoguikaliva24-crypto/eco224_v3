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
    id = serializers.IntegerField(read_only=True)
    full_name = serializers.SerializerMethodField()
    matricule = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    classe = serializers.SerializerMethodField()
    annee_scolaire = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ["id", "full_name", "matricule", "photo", "classe", "annee_scolaire"]

    def get_full_name(self, obj):
        v = (obj.full_name or "").strip()
        if v:
            return v
        return f"{(obj.prenom1 or '').strip()} {(obj.nom or '').strip()}".strip() or "Nom non défini"

    def get_matricule(self, obj):
        v = (obj.matricule or "").strip()
        return v if v else f"MAT-{obj.id}"

    def get_photo(self, obj):
        if not obj.photo:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.photo.url)
        return obj.photo.url

    def get_classe(self, obj):
        c = getattr(obj, "classe", None)
        if c:
            return getattr(c, "nom", str(c))
        return "Non définie"

    def get_annee_scolaire(self, obj):
        a = getattr(obj, "annee_scolaire", None)
        if a:
            return getattr(a, "libelle", str(a))
        return "Non définie"