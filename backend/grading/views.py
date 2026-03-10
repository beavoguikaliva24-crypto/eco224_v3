from django.shortcuts import render, get_object_or_404
from enrollment.models import Affectation
from .models import Periode,Note
from discipline.services import obtenir_bilan_discipline
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from .serializers import NoteSerializer
from .services import (
    calculer_bulletin_intelligent, 
    calculer_moyenne_annuelle_eleve, 
    calculer_rangs_classe_custom,
    calculer_stats_classe
)

class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class BulletinDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, affectation_id, periode_id=None):
        # 1. Récupération des données de base
        aff_cible = get_object_or_404(Affectation, pk=affectation_id)
        camarades = Affectation.objects.filter(
            classe=aff_cible.classe, 
            annee_scolaire=aff_cible.annee_scolaire
        )
        
        # 2. Distinction Périodique vs Annuel
        periode = None
        if periode_id:
            periode = get_object_or_404(Periode, pk=periode_id)
            data = calculer_bulletin_intelligent(aff_cible, periode)
            type_b = "periode"
            titre = f"Bulletin {periode.nom}"
        else:
            data = calculer_moyenne_annuelle_eleve(aff_cible)
            # Pour l'annuel, data contient 'moyenne_annuelle', on l'aligne
            data['moyenne_generale'] = data['moyenne_annuelle'] 
            type_b = "annuel"
            titre = "Bulletin Annuel"

        # 3. Calculs transversaux (Rang, Stats, Discipline)
        rangs = calculer_rangs_classe_custom(camarades, type_bulletin=type_b, periode=periode)
        stats = calculer_stats_classe(camarades, type_bulletin=type_b, periode=periode)
        bilan_disc = obtenir_bilan_discipline(aff_cible, periode)

        # 4. Construction du dictionnaire de réponse
        resultat = {
            "titre": titre,
            "eleve_nom": aff_cible.eleve.full_name,
            "classe_nom": aff_cible.classe.nom,
            "moyenne_generale": data['moyenne_generale'],
            "rang": rangs.get(aff_cible.id, "N/A"),
            "is_annuel": periode_id is None,
            "stats_classe": stats,
            "discipline": bilan_disc,
            "details": data.get('details', []) # Liste des notes par matière
        }

        # 5. Envoi au Serializer et réponse
        serializer = BulletinFullSerializer(resultat)
        return Response(serializer.data)

def calculer_stats_classe(camarades, type_bulletin="periode", periode=None):
    """
    Calcule la moyenne de la classe, la plus forte et la plus faible moyenne.
    """
    moyennes = []
    for aff in camarades:
        if type_bulletin == "periode":
            m = calculer_bulletin_intelligent(aff, periode)['moyenne_generale']
        else:
            m = calculer_moyenne_annuelle_eleve(aff)['moyenne_annuelle']
        moyennes.append(m)

    if not moyennes:
        return {"max": 0, "min": 0, "moyenne_classe": 0}

    return {
        "max": max(moyennes),
        "min": min(moyennes),
        "moyenne_classe": round(sum(moyennes) / len(moyennes), 2)
    }