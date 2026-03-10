from django.db import models
from enrollment.models import Affectation
from school.models import MatiereClasse, Periode
from django.core.exceptions import ValidationError

# Create your models here.
class Note(models.Model):
    affectation = models.ForeignKey(Affectation, on_delete=models.CASCADE, verbose_name="Affectation")
    matiereclasse = models.ForeignKey(MatiereClasse, on_delete=models.CASCADE, verbose_name="Matière-Classe")
    periodicite = models.ForeignKey(Periode, on_delete=models.CASCADE, verbose_name="Période")
    note1 = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True, verbose_name="Note 1")
    note2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Note 2")
    moyenne = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Moyenne")
    appreciation = models.CharField(max_length=255, null=True, blank=True, verbose_name="Appréciation")

    def get_appreciation(self,moyenne,bareme):
        ratio = moyenne / bareme
        if ratio >= 0.9: return "Excellent"
        elif ratio >= 0.8: return "Très bien"
        elif ratio >= 0.7: return "Bien"
        elif ratio >= 0.6: return "Assez bien"
        elif ratio >= 0.5: return "Passable"
        elif ratio >= 0.4: return "Insuffisant"
        else: return "Mediocre"

    def clean(self):
        # Vérifier si l'élève de l'affectation est bien actif
        if not self.affectation.eleve.is_active:
            raise ValidationError("Impossible d'ajouter une note : l'élève est désactivé.")
        
        # Vérifier si la matière enseignée correspond bien à la classe de l'élève
        # (Exemple : ne pas mettre une note de Physique de Terminale à un élève de 6ème)
        if self.matiereclasse.classe != self.affectation.classe:
            raise ValidationError(f"Erreur : Cette matière n'est pas enseignée en {self.affectation.classe.nom}.")
        
        bareme = self.affectation.classe.get_bareme()
        if self.note1 > bareme or self.note2 > bareme:
            raise ValidationError(f"Les notes ne peuvent pas dépasser le barème de {bareme} pour cette classe.")

    def save(self, *args, **kwargs):
        # Calcul de la moyenne
        if self.note1 is not None and self.note2 is not None:
            notes = [self.note1, self.note2]
            self.moyenne = sum(notes) / len(notes)
            self.appreciation = self.get_appreciation(self.moyenne, self.affectation.classe.get_bareme())
        else:
            self.moyenne = None
            self.appreciation = None

        self.full_clean()  # Assure que les validations sont respectées avant de sauvegarder
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        unique_together = ('affectation', 'matiereclasse', 'periodicite')  # Un élève ne peut avoir qu'une note par matière et période

    def __str__(self):
        return f"Note de {self.affectation.eleve.full_name} en {self.matiereclasse.matiere.nom} - {self.affectation.classe.nom} Année scolaire: {self.matiereclasse.annee_scolaire.annee_scolaire} - Période: {self.periodicite.nom} - Note1: {self.note1} - Note2: {self.note2} - Moyenne: {self.moyenne} - Appréciation: {self.appreciation}"
    
class BulletinPeriodique(models.Model):
    affectation = models.ForeignKey(Affectation, on_delete=models.CASCADE, verbose_name="Affectation")
    periode = models.ForeignKey(Periode, on_delete=models.CASCADE, verbose_name="Période")
    moyenne_generale = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Moyenne générale")
    rang = models.CharField(max_length=20, null=True, blank=True, verbose_name="Rang")
    appreciation_generale = models.CharField(max_length=255, null=True, blank=True, verbose_name="Appréciation générale")
    details_notes = models.JSONField(default=dict, verbose_name="Détails des notes par matière")
    stats_classe = models.JSONField(default=dict, verbose_name="Statistiques de la classe")
    date_calcul = models.DateTimeField(auto_now_add=True, verbose_name="Date de calcul")

    class Meta:
        verbose_name = "Bulletin périodique"
        verbose_name_plural = "Bulletins périodiques"
        unique_together = ('affectation', 'periode')  # Un bulletin par élève et période

    def __str__(self):
        return f"Bulletin de {self.affectation.eleve.full_name} - {self.affectation.classe.nom} - Période: {self.periode.nom} - Moyenne générale: {self.moyenne_generale} - Appréciation générale: {self.appreciation_generale}"
    
class BulletinAnnuel(models.Model):
    affectation = models.ForeignKey(Affectation, on_delete=models.CASCADE, verbose_name="Affectation")
    moyenne_annuelle = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Moyenne annuelle")
    rang = models.CharField(max_length=20, null=True, blank=True, verbose_name="Rang annuel")
    appreciation_annuelle = models.CharField(max_length=255, null=True, blank=True, verbose_name="Appréciation annuelle")
    date_calcul = models.DateTimeField(auto_now_add=True, verbose_name="Date de calcul")

    class Meta:
        verbose_name = "Bulletin annuel"
        verbose_name_plural = "Bulletins annuels"
        unique_together = ('affectation', 'annee_scolaire')  # Un bulletin annuel par élève et année scolaire

    def __str__(self):
        return f"Bulletin annuel de {self.affectation.eleve.full_name} - {self.affectation.classe.nom} - Année scolaire: {self.affectation.annee_scolaire.annee_scolaire} - Moyenne annuelle: {self.moyenne_annuelle} - Appréciation annuelle: {self.appreciation_annuelle}"




