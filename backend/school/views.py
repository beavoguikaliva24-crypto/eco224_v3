from rest_framework import viewsets, permissions
from .models import AnneeScolaire, Periode, Classe, Matiere, MatiereClasse
from .serializers import (
    AnneeScolaireSerializer, PeriodeSerializer, ClasseSerializer,
    MatiereSerializer, MatiereClasseSerializer
)

class AnneeScolaireViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = AnneeScolaire.objects.all()
    serializer_class = AnneeScolaireSerializer

class PeriodeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Periode.objects.all()
    serializer_class = PeriodeSerializer

class ClasseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer

class MatiereViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

class MatiereClasseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = MatiereClasse.objects.all()
    serializer_class = MatiereClasseSerializer