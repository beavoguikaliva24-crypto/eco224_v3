from rest_framework import serializers
from .models import Note, BulletinPeriode, BulletinAnnuel

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

# REMPLACE BulletinFullSerializer
class BulletinPeriodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulletinPeriode
        fields = '__all__'
        depth = 1 # Pour afficher les détails des objets liés (affectation, periode)

# REMPLACE BulletinFullSerializer
class BulletinAnnuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulletinAnnuel
        fields = '__all__'
        depth = 1