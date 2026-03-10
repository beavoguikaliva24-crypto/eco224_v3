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

    # ✅ photo élève (pas user.photo)
    photo = serializers.SerializerMethodField()

    # ✅ nouveaux champs demandés
    classe = serializers.SerializerMethodField()
    annee_scolaire = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "full_name",
            "matricule",
            "photo",
            "classe",
            "annee_scolaire",
        ]

    def get_full_name(self, obj):
        value = (obj.full_name or "").strip()
        if value:
            return value
        return f"{(obj.prenom1 or '').strip()} {(obj.nom or '').strip()}".strip() or "Nom non défini"

    def get_matricule(self, obj):
        value = (obj.matricule or "").strip()
        return value if value else f"MAT-{obj.id}"

    def get_photo(self, obj):
        if not obj.photo:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.photo.url)
        return obj.photo.url

    def get_classe(self, obj):
        # selon ton modèle de scolarité (Affectation/Classe)
        affectation = getattr(obj, "affectation_actuelle", None)
        if affectation and getattr(affectation, "classe", None):
            return affectation.classe.nom
        # fallback si relation directe existe
        if hasattr(obj, "classe") and obj.classe:
            return getattr(obj.classe, "nom", None) or str(obj.classe)
        return "Non définie"

    def get_annee_scolaire(self, obj):
        affectation = getattr(obj, "affectation_actuelle", None)
        if affectation and getattr(affectation, "annee_scolaire", None):
            return getattr(affectation.annee_scolaire, "libelle", None) or str(affectation.annee_scolaire)
        if hasattr(obj, "annee_scolaire") and obj.annee_scolaire:
            return getattr(obj.annee_scolaire, "libelle", None) or str(obj.annee_scolaire)
        return "Non définie"