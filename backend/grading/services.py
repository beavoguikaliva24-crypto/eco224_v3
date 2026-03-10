from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .models import BulletinPeriodique, BulletinAnnuel, Note
from enrollment.models import Affectation
from school.models import MatiereClasse, Periode
from discipline.services import obtenir_bilan_discipline

def calculer_bulletin_intelligent(affectation, periode):
    # 1. On liste toutes les matières prévues pour la classe
    matieres_programme = MatiereClasse.objects.filter(
        classe=affectation.classe,
        annee_scolaire=affectation.annee_scolaire
    )
    
    total_points_eleve = 0
    total_coefficients_programme = 0
    details = []

    for mc in matieres_programme:
        coef = mc.coefficient
        total_coefficients_programme += coef

        note_eleve = Note.objects.filter(
            affectation=affectation, 
            matiereclasse=mc, 
            periodicite=periode
        ).first()
        
        evaluation_existe_dans_classe = Note.objects.filter(
            matiereclasse=mc,
            periodicite=periode,
            affectation__classe=affectation.classe
        ).exists()

        if note_eleve and note_eleve.moyenne is not None:
            points = note_eleve.moyenne * coef
            moyenne_affichable = note_eleve.moyenne
            appreciation = note_eleve.appreciation
            total_points_eleve += points
        elif not evaluation_existe_dans_classe:
            total_coefficients_programme -= coef
            moyenne_affichable = "Non évalué"
            appreciation = "Saisie non effectuée"
            points = None
        else:
            points = 0
            moyenne_affichable = 0
            appreciation = "Absent / Non noté"
            total_points_eleve += 0

        details.append({
            'matiere': mc.matiere.nom,
            'moyenne': moyenne_affichable,
            'coef': coef,
            'points': points if points is not None else "N/A",
            'appreciation': appreciation
        })

    moyenne_generale = total_points_eleve / total_coefficients_programme if total_coefficients_programme > 0 else 0
    
    return {
        'moyenne_generale': round(moyenne_generale, 2),
        'details': details,
        'coef_total_calcule': total_coefficients_programme
    }

def calculer_moyenne_annuelle_eleve(affectation):
    periodes = Periode.objects.filter(annee_scolaire=affectation.annee_scolaire).order_by('id')
    somme_moyennes = 0
    periodes_comptees = 0
    resultats_periodes = []

    for periode in periodes:
        data = calculer_bulletin_intelligent(affectation, periode)
        if data['coef_total_calcule'] > 0:
            somme_moyennes += data['moyenne_generale']
            periodes_comptees += 1
            resultats_periodes.append({
                'nom': periode.nom,
                'moyenne': float(data['moyenne_generale'])
            })

    moyenne_annuelle = somme_moyennes / periodes_comptees if periodes_comptees > 0 else 0
    
    return {
        'moyenne_annuelle': round(moyenne_annuelle, 2),
        'details_periodes': resultats_periodes
    }

def calculer_rangs_classe_custom(affectations_classe, type_bulletin="periode", periode=None):
    scores = []
    for aff in affectations_classe:
        if type_bulletin == "periode":
            moy = calculer_bulletin_intelligent(aff, periode)['moyenne_generale']
        else:
            moy = calculer_moyenne_annuelle_eleve(aff)['moyenne_annuelle']
        scores.append({'affectation_id': aff.id, 'moyenne': moy})

    scores.sort(key=lambda x: x['moyenne'], reverse=True)
    rangs = {}
    current_rang = 0
    last_moyenne = -1

    for score in scores:
        if score['moyenne'] != last_moyenne:
            current_rang += 1
        
        nb_ex_aequo = sum(1 for s in scores if s['moyenne'] == score['moyenne'])
        suffixe = "er" if current_rang == 1 else "ème"
        mention_ex = " ex" if nb_ex_aequo > 1 else ""
        rangs[score['affectation_id']] = f"{current_rang}{suffixe}{mention_ex}"
        last_moyenne = score['moyenne']
    
    return rangs

def calculer_stats_classe(camarades, type_bulletin="periode", periode=None):
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
        "max": float(max(moyennes)),
        "min": float(min(moyennes)),
        "moyenne_classe": float(round(sum(moyennes) / len(moyennes), 2))
    }

# --- FONCTIONS DE GÉNÉRATION ET SAUVEGARDE (CELLES QUI MANQUAIENT) ---

def generer_et_sauvegarder_bulletin_periodique(affectation_id: int, periode_id: int):
    affectation = get_object_or_404(Affectation, pk=affectation_id)
    periode = get_object_or_404(Periode, pk=periode_id)
    camarades = Affectation.objects.filter(classe=affectation.classe, annee_scolaire=affectation.annee_scolaire)

    data_bulletin = calculer_bulletin_intelligent(affectation, periode)
    rangs = calculer_rangs_classe_custom(camarades, type_bulletin="periode", periode=periode)
    stats = calculer_stats_classe(camarades, type_bulletin="periode", periode=periode)
    bilan_disc = obtenir_bilan_discipline(affectation, periode)

    bulletin_obj, created = BulletinPeriodique.objects.update_or_create(
        affectation=affectation,
        periode=periode,
        defaults={
            'moyenne_generale': data_bulletin.get('moyenne_generale', 0.0),
            'rang': rangs.get(affectation.id, "N/A"),
            'details_notes': data_bulletin.get('details', []),
            'stats_classe': stats,
            'appreciation_generale': bilan_disc.get('appreciation', "RAS"),
        }
    )
    return bulletin_obj

def generer_et_sauvegarder_bulletin_annuel(affectation_id: int):
    affectation = get_object_or_404(Affectation, pk=affectation_id)
    camarades = Affectation.objects.filter(classe=affectation.classe, annee_scolaire=affectation.annee_scolaire)

    data_annuel = calculer_moyenne_annuelle_eleve(affectation)
    rangs_annuels = calculer_rangs_classe_custom(camarades, type_bulletin="annuel")

    bulletin_obj, created = BulletinAnnuel.objects.update_or_create(
        affectation=affectation,
        defaults={
            'moyenne_annuelle': data_annuel.get('moyenne_annuelle', 0.0),
            'rang': rangs_annuels.get(affectation.id, "N/A"),
            # 'appreciation_annuelle': # Logique à définir si nécessaire
        }
    )
    return bulletin_obj