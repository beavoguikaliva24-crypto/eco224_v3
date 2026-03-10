from django.db import models
from school.models import *
from people.models import *

# Create your models here.
class TypeAffectation(models.TextChoices):
    INSCRIPTION = 'INSCRIPTION', 'Inscription'
    REINSCRIPTION = 'REINSCRIPTION', 'Réinscription'
    AUTRE = 'AUTRE', 'Autre'

class EtatAffectation(models.TextChoices):
    NOUVEAU = 'NOUVEAU', 'Nouveau/lle'
    ADMIS = 'ADMIS', 'Admis/e'
    NON_ADMIS = 'NON_ADMIS', 'Non admis/e'
    REDOUBLANT = 'REDOUBLANT', 'Redoublant/e'
    CANDIDAT_LIBRE = 'CANDIDAT_LIBRE', 'Candidat/e libre'
    TRANSFERE = 'TRANSFERE', 'Transféré/e'
    AUTRE = 'AUTRE', 'Autre'

class StatutAffectation(models.TextChoices):
    ACTIF = 'ACTIF', 'Actif'
    INACTIF = 'INACTIF', 'Inactif'
    ABANDON = 'ABANDON', 'Abandon'
    TRANSFERE = 'TRANSFERE', 'Transféré/e'

class Affectation(models.Model):
    eleve = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Élève")
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, verbose_name="Classe")
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE, verbose_name="Année scolaire")
    type_affectation = models.CharField(max_length=20, choices=TypeAffectation.choices, verbose_name="Type d'affectation")
    frais_type = models.IntegerField(default=0, verbose_name="Frais de type d'affectation")
    etat_affectation = models.CharField(max_length=20, choices=EtatAffectation.choices, verbose_name="État de l'affectation")
    date_affectation = models.DateField(auto_now_add=True, verbose_name="Date d'affectation")
    statut_affectation = models.CharField(max_length=20, choices=StatutAffectation.choices, verbose_name="Statut de l'affectation")

    class Meta:
        verbose_name = "Affectation"
        verbose_name_plural = "Affectations"
        unique_together = ('eleve', 'annee_scolaire')  # Un élève ne peut être affecté qu'une seule fois par année scolaire

    def __str__(self):
        return f"{self.eleve.full_name} - {self.classe.nom} ({self.annee_scolaire.annee_scolaire}) - {self.type_affectation} - {self.etat_affectation} - {self.statut_affectation}"





