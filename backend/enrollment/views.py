from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Affectation
from .serializers import AffectationSerializer

class AffectationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Affectation.objects.all()
    serializer_class = AffectationSerializer