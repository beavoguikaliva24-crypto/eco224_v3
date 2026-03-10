from django.db.models import Sum, F
from django.shortcuts import get_object_or_404
from .models import BulletinAnnuel, Note, BulletinPeriode
from enrollment.models import Affectation
from school.models import MatiereClasse, Periode
from discipline.services import obtenir_bilan_discipline

from django.db.models import Exists, OuterRef
from .models import Note, MatiereClasse

def calculer_bulletin_intelligent(affectation, periode):
    # 1. On liste toutes les matières prévues pour la classe
    matieres_programme = MatiereClasse.objects.filter(
        classe=affectation.classe,
        annee_scolaire=affectation.annee_scolaire
    )
    
    total_points = 0
    total_coefficients_actifs = 0
    details = []

    for mc in matieres_programme:
        coef = mc.coefficient
        
        # On vérifie si l'élève a une note
        note_eleve = Note.objects.filter(
            affectation=affectation, 
            matiereclasse=mc, 
            periodicite=periode
        ).first()

        # SECURITÉ : Est-ce qu'au moins un élève de la classe a une note dans cette matière ?
        # Si personne n'a de note, c'est que le prof n'a pas encore fait la saisie.
        evaluation_existe_dans_classe = Note.objects.filter(
            matiereclasse=mc,
            periodicite=periode,
            affectation__classe=affectation.classe
        ).exists()

        if note_eleve and note_eleve.moyenne is not None:
            # Cas normal : l'élève a une note
            points = note_eleve.moyenne * coef
            moyenne_affis = note_eleve.moyenne
            appreciation = note_eleve.appreciation
            total_coefficients_actifs += coef
            total_points += points
        elif not evaluation_existe_dans_classe:
            # Cas "Saisie en cours" : Personne n'a de note, on ignore la matière
            moyenne_affis = "En attente"
            appreciation = "Saisie non effectuée"
            points = None # Ne compte pas dans le calcul
        else:
            # Cas "Absent" : La classe est notée, mais cet élève n'a rien -> 0/20
            moyenne_affis = 0
            appreciation = "Absent / Non noté"
            total_coefficients_actifs += coef
            total_points += 0 # L'élève prend 0

        details.append({
            'matiere': mc.matiere.nom,
            'moyenne': moyenne_affis,
            'coef': coef,
            'points': points,
            'appreciation': appreciation
        })

    # Calcul final sur les coefficients réellement évalués
    moyenne_generale = total_points / total_coefficients_actifs if total_coefficients_actifs > 0 else 0
    
    return {
        'moyenne_generale': round(moyenne_generale, 2),
        'details': details,
        'coef_total': total_coefficients_actifs
    }

def calculer_moyenne_annuelle_eleve(affectation):
    """
    Calcule la moyenne annuelle en agrégeant les résultats de chaque période.
    """
    # 1. Récupérer toutes les périodes de l'année scolaire en cours
    periodes = Periode.objects.filter(annee_scolaire=affectation.annee_scolaire).order_by('id')
    
    somme_moyennes = 0
    periodes_comptees = 0
    resultats_periodes = []

    for periode in periodes:
        # On calcule le bulletin pour cette période spécifique
        data = calculer_bulletin_intelligent(affectation, periode)
        
        # On ne compte la période que si elle contient au moins une note
        if data['coef_total'] > 0:
            somme_moyennes += data['moyenne_generale']
            periodes_comptees += 1
            resultats_periodes.append({
                'nom': periode.nom,
                'moyenne': data['moyenne_generale']
            })

    # Calcul final
    moyenne_annuelle = somme_moyennes / periodes_comptees if periodes_comptees > 0 else 0
    
    return {
        'moyenne_annuelle': round(moyenne_annuelle, 2),
        'details_periodes': resultats_periodes,
        'nb_periodes': periodes_comptees
    }

def calculer_rangs_classe_custom(affectations_classe, type_bulletin="periode", periode=None):
    """
    Calcule les rangs selon votre logique : 1er, 2ème, 2ème ex, 3ème, 4ème...
    """
    scores = []
    for aff in affectations_classe:
        # Import local pour éviter les imports circulaires
        from grading.services import calculer_bulletin_intelligent, calculer_moyenne_annuelle_eleve
        
        if type_bulletin == "periode":
            moy = calculer_bulletin_intelligent(aff, periode)['moyenne_generale']
        else:
            moy = calculer_moyenne_annuelle_eleve(aff)['moyenne_annuelle']
        scores.append({'affectation_id': aff.id, 'moyenne': moy})

    # Tri par moyenne décroissante
    scores.sort(key=lambda x: x['moyenne'], reverse=True)

    rangs = {}
    current_rang = 0
    derniere_moyenne = None

    for i, score in enumerate(scores):
        # On n'augmente le chiffre du rang que si la moyenne est différente
        if score['moyenne'] != derniere_moyenne:
            current_rang += 1
            derniere_moyenne = score['moyenne']
        
        # On compte combien d'élèves ont cette même moyenne
        nb_ex_aequo = sum(1 for s in scores if s['moyenne'] == score['moyenne'])
        
        # Construction de la chaîne (1er, 2ème, etc.)
        suffixe = "er" if current_rang == 1 else "ème"
        mention_ex = " ex" if nb_ex_aequo > 1 else ""
        
        rangs[score['affectation_id']] = f"{current_rang}{suffixe}{mention_ex}"
    
    return rangs

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

def generer_et_sauvegarder_bulletin_periode(affectation_id: int, periode_id: int):
    """
    Calcule toutes les données d'un bulletin périodique et le sauvegarde en base de données.
    Retourne l'instance du bulletin nouvellement créé ou mis à jour.
    """
    affectation = get_object_or_404(Affectation, pk=affectation_id)
    periode = get_object_or_404(Periode, pk=periode_id)
    camarades = Affectation.objects.filter(
        classe=affectation.classe, 
        annee_scolaire=affectation.annee_scolaire
    )

    # 1. Calculs (réutilisation de votre logique existante)
    data_bulletin = calculer_bulletin_intelligent(affectation, periode)
    rangs = calculer_rangs_classe_custom(camarades, type_bulletin="periode", periode=periode)
    stats = calculer_stats_classe(camarades, type_bulletin="periode", periode=periode)
    bilan_disc = obtenir_bilan_discipline(affectation, periode)

    # 2. Sauvegarde avec update_or_create pour éviter les doublons
    bulletin_obj, created = BulletinPeriode.objects.update_or_create(
        affectation=affectation,
        periode=periode,
        defaults={
            'moyenne_generale': data_bulletin.get('moyenne_generale', 0.0),
            'rang': rangs.get(affectation.id, "N/A"),
            'details_notes': data_bulletin.get('details', {}),
            'stats_classe': stats,
            'discipline': bilan_disc,
        }
    )
    return bulletin_obj

def generer_et_sauvegarder_bulletin_annuel(affectation_id: int):
    """
    Calcule les données d'un bulletin annuel et le sauvegarde en base de données.
    """
    affectation = get_object_or_404(Affectation, pk=affectation_id)
    camarades = Affectation.objects.filter(
        classe=affectation.classe, 
        annee_scolaire=affectation.annee_scolaire
    )

    # 1. Calculs
    data_annuel = calculer_moyenne_annuelle_eleve(affectation)
    rangs_annuels = calculer_rangs_classe_custom(camarades, type_bulletin="annuel")

    # 2. Sauvegarde
    bulletin_obj, created = BulletinAnnuel.objects.update_or_create(
        affectation=affectation,
        defaults={
            'moyenne_annuelle': data_annuel.get('moyenne_annuelle', 0.0),
            'rang_annuel': rangs_annuels.get(affectation.id, "N/A"),
            'details_periodes': data_annuel.get('details_periodes', {}),
        }
    )
    return bulletin_obj