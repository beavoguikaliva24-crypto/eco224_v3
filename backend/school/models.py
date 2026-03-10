from datetime import date
from django.db import models
from django.forms import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from people.models import *

# Create your models here.
class CycleScolaire(models.TextChoices):
    CRECHE = 'Crèche', 'Crèche'
    MATERNELLE = 'Maternelle', 'Maternelle'
    PRIMAIRE = 'Primaire', 'Primaire'
    COLLEGE = 'Collège', 'Collège'
    LYCEE = 'Lycée', 'Lycée'
    UNIVERSITE = 'Université', 'Université'
    AUTRE = 'Autre', 'Autre'

class OptionScolaire(models.TextChoices):
    SCIENCES_EXPERIMENTALES = 'Sciences expérimentales', 'Sciences expérimentales'
    SCIENCES_MATHEMATIQUES = 'Sciences mathématiques', 'Sciences mathématiques'
    SCIENCES_SOCIALES = 'Sciences sociales', 'Sciences sociales'
    SCIENTIFIQUE = 'Scientifique', 'Scientifique'
    LITTERAIRE = 'Littéraire', 'Littéraire'
    TECHNIQUE = 'Technique', 'Technique'
    GENERALE = 'Générale', 'Générale'
    TRON_COMMUN = 'Tron commun', 'Tron commun'
    AUTRE = 'Autre', 'Autre'
    SANS_OPTION = 'Sans option', 'Sans option'

class TypePeriode(models.TextChoices):
    TRIMESTRE = 'Trimestre', 'Trimestre'
    SEMESTRE = 'Semestre', 'Semestre'
    ANNEE = 'Année', 'Année'
    AUTRE = 'Autre', 'Autre'

# Fonctions utilitaires
def type_par_cycle(cycle):
    if cycle in [CycleScolaire.CRECHE, CycleScolaire.MATERNELLE, CycleScolaire.PRIMAIRE]: 
        return TypePeriode.TRIMESTRE
    elif cycle in [CycleScolaire.COLLEGE, CycleScolaire.LYCEE]:
        return TypePeriode.SEMESTRE
    
def bareme_par_cycle(cycle):
    if cycle in [CycleScolaire.CRECHE, CycleScolaire.MATERNELLE, CycleScolaire.PRIMAIRE]:
        return 10
    elif cycle in [CycleScolaire.COLLEGE, CycleScolaire.LYCEE]:
        return 20
    
class AnneeScolaire(models.Model):
    annee_scolaire = models.CharField(max_length=9, unique=True, null=True, blank=True, verbose_name="Année scolaire")
    debut_annee = models.IntegerField(verbose_name="Année de début")
    fin_annee = models.IntegerField(verbose_name="Année de fin")

    def clean(self):
        super().clean() # Appelle la validation de base
        if self.debut_annee is not None and self.fin_annee is not None: # Vérifie que les deux années sont présentes
            if self.fin_annee != self.debut_annee + 1: # Vérifie que l'année de fin est exactement un an après l'année de début
                raise ValidationError("L'année de fin doit être exactement un an après l'année de début.")
            if not ( 2020 <= self.debut_annee <= 2050) or not (2021 <= self.fin_annee <= 2051): # Vérifie que les années sont dans la plage acceptable
                raise ValidationError("L'année doit être entre 2020 et 2051.")
            if (self.fin_annee - self.debut_annee) != 1: # Vérifie que l'écart entre les années est de 1
                raise ValidationError("L'année de fin doit être exactement un an après l'année de début.")
        
    def save(self, *args, **kwargs):
        self.annee_scolaire = f"{self.debut_annee}-{self.fin_annee}"
        self.full_clean()  # Valide les données avant de sauvegarder
        super().save(*args, **kwargs)

    def __str__(self):
        return self.annee_scolaire or "Année scolaire non définie"
    
class Periode(models.Model):
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE, related_name='periodes', verbose_name="Année scolaire")
    cycle_scolaire = models.CharField(max_length=20, choices=CycleScolaire.choices, verbose_name="Cycle scolaire")
    type_periode = models.CharField(max_length=20, choices=TypePeriode.choices, verbose_name="Type de période")
    nom = models.CharField(max_length=50, verbose_name="Nom de la période (ex: 1er trimestre, 2ème semestre, etc.)")
    ordre = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], verbose_name="Ordre de la période dans l'année scolaire (ex: 1 pour le 1er trimestre, 2 pour le 2ème trimestre, etc.)")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")

    class Meta:
        unique_together = ('annee_scolaire', 'cycle_scolaire', 'type_periode', 'nom') # Assure l'unicité de la période

    def __str__(self):
        return f"{self.cycle_scolaire} ({self.type_periode}) - {self.nom} - {self.annee_scolaire}"

class Classe(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    nom = models.CharField(max_length=100, verbose_name="Nom de la classe")
    cycle_scolaire = models.CharField(max_length=20, choices=CycleScolaire.choices, verbose_name="Cycle scolaire")
    option_scolaire = models.CharField(max_length=30, choices=OptionScolaire.choices, verbose_name="Option scolaire", null=True, blank=True)
    est_active = models.BooleanField(default=True, verbose_name="Classe active")

    def get_bareme(self):
        # Méthode pour récupérer le barème de la classe (ex: nombre de points pour chaque note)
        if self.cycle_scolaire in ["Crèche", "Maternelle", "Primaire"]:
            return 10
        if self.cycle_scolaire in ["Collège", "Lycée"]:
            return 20
        return 20

    def __str__(self):
        return f"{self.nom} - {self.cycle_scolaire} - {self.option_scolaire or 'Sans option'} - {'Active' if self.est_active else 'Inactive'}"
        

class Matiere(models.Model):
    code = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Code")
    nom = models.CharField(max_length=100, verbose_name="Nom de la matière")
    est_active = models.BooleanField(default=True, verbose_name="Matière active")

    def __str__(self):
        return f"{self.nom} - {'Active' if self.est_active else 'Inactive'}"

class MatiereClasse(models.Model):
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE, related_name='matieres_classe', verbose_name="Année scolaire")
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='matieres_classe', verbose_name="Classe")
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='classes_matiere', verbose_name="Matière")
    professeur = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='matieres_enseignees', verbose_name="Professeur")
    coefficient = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Coefficient")
    est_active = models.BooleanField(default=True, verbose_name="Matière active dans la classe")

    class Meta:
        unique_together = ('annee_scolaire', 'classe', 'matiere') # Assure qu'une matière ne peut être associée qu'une seule fois à une classe pour une année scolaire donnée
        ordering = ['annee_scolaire__debut_annee', 'classe__nom', 'matiere__nom'] # Tri par année scolaire, puis par nom de classe, puis par nom de matière

    def __str__(self):
        return f"{self.annee_scolaire} - {self.matiere.nom} pour {self.classe.nom} - {'Active' if self.est_active else 'Inactive'}"


