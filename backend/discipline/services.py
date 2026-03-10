# discipline/services.py
from .models import Discipline
from django.db.models import Sum


def obtenir_bilan_discipline(affectation, periode=None):
    query = Discipline.objects.filter(affectation=affectation)

    # Somme des points perdus
    total_points_perdus = query.aggregate(total=Sum('points_perdus'))['total'] or 0
    
    # Calcul de la note de conduite (ne peut pas descendre en dessous de 0)
    note_conduite = max(20 - total_points_perdus, 0)
    
    # Déterminer une appréciation automatique
    if note_conduite >= 18: appreciation = "Excellente"
    elif note_conduite >= 14: appreciation = "Bonne"
    elif note_conduite >= 10: appreciation = "Passable"
    else: appreciation = "À surveiller"

    return {
        'total_absences': query.filter(type_incident='ABSENCE').count(),
        'total_retards': query.filter(type_incident='RETARD').count(),
        'total_indisciplines': query.filter(type_incident='COMPORTEMENT').count(),
        'note_conduite': note_conduite,
        'appreciation_conduite': appreciation
    }