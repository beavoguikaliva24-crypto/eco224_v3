from rest_framework import serializers
from .models import AnneeScolaire, Periode, Classe, Matiere, MatiereClasse

class AnneeScolaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnneeScolaire
        fields = "__all__"

class PeriodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periode
        fields = "__all__"

class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = "__all__"

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = "__all__"

class MatiereClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatiereClasse
        fields = "__all__"