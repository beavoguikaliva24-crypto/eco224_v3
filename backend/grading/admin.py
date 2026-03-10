from django.contrib import admin
from .models import Note, BulletinPeriode, BulletinAnnuel

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # On utilise la notation __ pour accéder aux champs des modèles liés
    list_display = ("id", "get_eleve_name", "get_matiere_name", "periodicite", "note1", "note2", "moyenne")
    list_filter = ("affectation__classe", "periodicite", "matiereclasse__matiere")
    search_fields = ("affectation__eleve__user__first_name", "affectation__eleve__user__last_name", "matiereclasse__matiere__nom")

    # Fonctions pour obtenir les noms pour un affichage plus propre
    @admin.display(description="Élève")
    def get_eleve_name(self, obj):
        return obj.affectation.eleve.full_name

    @admin.display(description="Matière")
    def get_matiere_name(self, obj):
        return obj.matiereclasse.matiere.nom

# Enregistrement des nouveaux modèles pour qu'ils apparaissent dans l'admin
@admin.register(BulletinPeriode)
class BulletinPeriodeAdmin(admin.ModelAdmin):
    list_display = ('affectation', 'periode', 'moyenne_generale', 'rang', 'date_calcul')
    list_filter = ('affectation__classe', 'periode')

@admin.register(BulletinAnnuel)
class BulletinAnnuelAdmin(admin.ModelAdmin):
    list_display = ('affectation', 'moyenne_annuelle', 'rang', 'date_calcul')
    list_filter = ('affectation__classe',)