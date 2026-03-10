from django.shortcuts import render,redirect
from django.contrib import messages
from rest_framework import viewsets, permissions
from .models import FraisScolarite, Paiement, Versement
from .serializers import FraisScolariteSerializer, PaiementSerializer, VersementSerializer

class FraisScolariteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = FraisScolarite.objects.all()
    serializer_class = FraisScolariteSerializer

class PaiementViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer

class VersementViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Versement.objects.all()
    serializer_class = VersementSerializer

def recalculer_tous_les_paiements(request):
    """
    Force le recalcul de tous les dossiers de paiement 
    basé sur la configuration actuelle des frais.
    """
    paiements = Paiement.objects.all()
    compteur = 0
    
    for paiement in paiements:
        # En appelant save(), notre logique automatique 
        # va chercher les nouveaux FraisScolarite
        paiement.save()
        compteur += 1
        
    messages.success(request, f"Succès : {compteur} dossiers de paiement ont été mis à jour.")
    return redirect('liste_paiements_erreurs') # Redirige vers la liste des erreurs