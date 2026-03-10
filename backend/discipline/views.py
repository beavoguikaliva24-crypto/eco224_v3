from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Discipline
from .serializers import DisciplineSerializer

class DisciplineViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
