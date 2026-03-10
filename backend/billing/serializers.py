from rest_framework import serializers
from .models import FraisScolarite, Paiement, Versement

class FraisScolariteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraisScolarite
        fields = "__all__"

class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = "__all__"

class VersementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Versement
        fields = "__all__"