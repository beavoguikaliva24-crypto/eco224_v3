from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

class BulletinSerializer(serializers.Serializer):
    titre = serializers.CharField()
    moyenne_eleve = serializers.FloatField()
    rang = serializers.CharField()
    # Statistiques de la classe
    stats_classe = serializers.DictField()
    # Détails des matières
    details = serializers.ListField()
    # Discipline
    discipline = serializers.DictField()