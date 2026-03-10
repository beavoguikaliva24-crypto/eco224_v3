from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404

# Nouveaux imports
from .models import Note, BulletinPeriode, BulletinAnnuel
from .serializers import NoteSerializer, BulletinPeriodeSerializer, BulletinAnnuelSerializer
from .services import generer_et_sauvegarder_bulletin_periode, generer_et_sauvegarder_bulletin_annuel


class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class BulletinDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, affectation_id, periode_id=None):
        force_generation = request.query_params.get('force_generation', 'false').lower() == 'true'

        if periode_id:
            # --- Cas du Bulletin Périodique ---
            if not force_generation:
                try:
                    # Utilisation du bon nom de modèle : BulletinPeriodique
                    bulletin = BulletinPeriode.objects.get(affectation_id=affectation_id, periode_id=periode_id)
                    serializer = BulletinPeriodeSerializer(bulletin)
                    return Response(serializer.data)
                except BulletinPeriode.DoesNotExist:
                    pass

            # Appel de la bonne fonction de service
            bulletin = generer_et_sauvegarder_bulletin_periode(affectation_id, periode_id)
            serializer = BulletinPeriodeSerializer(bulletin)
            return Response(serializer.data)

        else:
            # --- Cas du Bulletin Annuel ---
            if not force_generation:
                try:
                    bulletin = BulletinAnnuel.objects.get(affectation_id=affectation_id)
                    serializer = BulletinAnnuelSerializer(bulletin)
                    return Response(serializer.data)
                except BulletinAnnuel.DoesNotExist:
                    pass
            
            bulletin = generer_et_sauvegarder_bulletin_annuel(affectation_id)
            serializer = BulletinAnnuelSerializer(bulletin)
            return Response(serializer.data)