from django.db import models
from enrollment.models import Affectation
from grading.models import Periode

# Create your models here.

class Discipline(models.Model):
    TYPE_INCIDENT = (
        ('ABSENCE', 'Absence'),
        ('RETARD', 'Retard'),
        ('COMPORTEMENT', 'Comportement/Indiscipline'),
        ('PRESENCE', 'Présence Exceptionnelle'), # Optionnel
    )

    affectation = models.ForeignKey(Affectation, on_delete=models.CASCADE, verbose_name="Élève")
    type_incident = models.CharField(max_length=20, choices=TYPE_INCIDENT, default='ABSENCE')
    # Pour les absences/retards
    justifie = models.BooleanField(default=False, verbose_name="Justifié ?")
    date_infraction = models.DateTimeField(auto_now_add=True, verbose_name="Date de l'infraction")
    type_infraction_choix = [
        ('Absence injustifiée', 'Absence injustifiée'),
        ('Retard', 'Retard'),
        ('Comportement inapproprié', 'Comportement inapproprié'),
    ]
    type_infraction = models.CharField(max_length=255, choices=type_infraction_choix, verbose_name="Type d'infraction")
    description = models.TextField(blank=True, null=True, verbose_name="Détails / Motif")
    sanction = models.CharField(max_length=255, verbose_name="Sanction appliquée")
    points_perdus = models.PositiveIntegerField(
        default=0, 
        help_text="Nombre de points à retirer du capital de 20"
    )
    # Pour le comportement
    commentaire = models.TextField(blank=True, null=True, verbose_name="Détails / Motif")

    class Meta:
        verbose_name = "Discipline"
        verbose_name_plural = "Discipline"
        ordering = ['-date_infraction']

    def __str__(self):
        return f"Infraction de {self.affectation.eleve.full_name} le {self.date_infraction.strftime('%Y-%m-%d')} - {self.description} - Sanction: {self.sanction}"
    
