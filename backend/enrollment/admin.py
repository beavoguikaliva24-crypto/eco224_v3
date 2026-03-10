from django.contrib import admin
from .models import Affectation

@admin.register(Affectation)
class AffectationAdmin(admin.ModelAdmin):
    list_display = ("id", "eleve", "classe", "annee_scolaire", "type_affectation", "etat_affectation", "statut_affectation")
    list_filter = ("annee_scolaire", "classe", "type_affectation", "etat_affectation", "statut_affectation")
    search_fields = ("eleve__full_name", "eleve__matricule", "classe__nom")