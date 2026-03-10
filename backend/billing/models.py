from decimal import Decimal
import uuid
import uuid

from django.db import models
from django.conf import settings
from school.models import *
from people.models import *
from enrollment.models import *

# Create your models here.

class FraisScolarite(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, verbose_name="Classe")
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE, verbose_name="Année scolaire")
    montant = models.BigIntegerField(default=0, verbose_name="Montant des frais de scolarité")
    tranche1 = models.BigIntegerField(default=0, verbose_name="Tranche 1")
    tranche2 = models.BigIntegerField(default=0, verbose_name="Tranche 2")
    tranche3 = models.BigIntegerField(default=0, verbose_name="Tranche 3")

    class Meta:
        verbose_name = "Frais de scolarité"
        verbose_name_plural = "Frais de scolarité"
        unique_together = ('classe', 'annee_scolaire')  # Un montant de frais de scolarité unique par classe et année scolaire

    def __str__(self):
        return f"Frais de scolarité pour {self.classe.nom} ({self.annee_scolaire.annee_scolaire}) : {self.montant} FCFA"  

class Paiement(models.Model):
    affectation = models.ForeignKey(Affectation, on_delete=models.CASCADE, verbose_name="Affectation") 
    reduction = models.SmallIntegerField(default=0, verbose_name="Pourcentage de la réduction")
    montant_paiement = models.BigIntegerField(default=0, verbose_name="Montant dû après réduction")
    tranche1 = models.BigIntegerField(default=0, verbose_name="Montant de la tranche 1")
    tranche2 = models.BigIntegerField(default=0, verbose_name="Montant de la tranche 2")
    tranche3 = models.BigIntegerField(default=0, verbose_name="Montant de la tranche 3")
    
    def save(self, *args, **kwargs):
        # 1. On récupère les frais de base depuis la configuration
        frais_base = FraisScolarite.objects.filter(
            annee_scolaire=self.affectation.annee_scolaire,
            classe=self.affectation.classe
        ).first()
        if frais_base:
            # 2. Calcul du multiplicateur de réduction (ex: 10% -> 0.9)
            # On s'assure que la réduction est entre 0 et 100
            val_reduction = Decimal(self.reduction or 0) / Decimal(100)
            val_reduction = max(Decimal(0), min(Decimal(1), val_reduction))
            multiplier = Decimal(1) - val_reduction

            # 3. On applique la réduction sur TOUT
            # Le montant total que l'élève doit réellement payer
            self.montant_paiement = frais_base.montant * multiplier
    
            # MISE À JOUR DES CHAMPS (Correction des noms ici)
            self.montant_paiement = frais_base.montant * multiplier
            self.tranche1 = frais_base.tranche1 * multiplier
            self.tranche2 = frais_base.tranche2 * multiplier
            self.tranche3 = frais_base.tranche3 * multiplier
        else:
            print("❌ Aucun frais trouvé")
        
        # NE PAS OUBLIER : Enregistrement effectif
        super().save(*args, **kwargs)

    @property
    def total_paye(self):
        # Somme de tous les versements liés
        from django.db.models import Sum
        # On utilise le related_name 'versements' défini dans TableVersement
        resultat = self.versements.aggregate(total=Sum('montant'))['total']
        return resultat or 0

    @property
    def reste_a_payer(self):
        return self.montant_paiement - self.total_paye

    @property
    def statut_paiement(self):
        reste = self.reste_a_payer
        if reste <= 0:
            return "✅ Soldé"
        elif reste < self.montant_paiement:
            return "🟠 Partiel"
        return "🔴 Impayé"

    def __str__(self):
        return f"Paiement {self.affectation.eleve.full_name} ({self.statut_paiement} - {self.affectation.classe.nom}) - Total dû: {self.montant_paiement} GN - Payé: {self.total_paye} GN - Reste: {self.reste_a_payer} GN"


class Versement(models.Model):
    paiement = models.ForeignKey(Paiement, on_delete=models.CASCADE, related_name='versements')
    montant = models.BigIntegerField(default=0, verbose_name="Montant du versement")
    date_versement = models.DateTimeField(auto_now_add=True)
    reference_recu = models.CharField(max_length=100, unique=True, editable=False)
    mode_paiement = models.CharField(max_length=20, choices=[('CASH', 'Espèces'), ('OM', 'Orange Money'), ('MOMO', 'Mobile Money'), ('VIREMENT', 'Virement'), ('CHEQUE', 'Chèque'), ('CARD', 'Carte bancaire'), ('AUT', 'Autre')], default='CASH')

    def clean(self):
        """
        Vérifie que le montant du versement ne dépasse pas le reste à payer.
        """
        if not self.pk:  # Uniquement lors de la création d'un NOUVEAU versement
            reste = self.paiement.reste_a_payer
            if self.montant > reste:
                raise ValidationError(
                    f"Impossible d'encaisser {self.montant} GN. "
                    f"Le reste à payer est de seulement {reste} GN."
                )
            
    def save(self, *args, **kwargs):
        # 1. Générer une référence unique si elle n'existe pas
        if not self.reference_recu:
            prefix = "REC"
            unique_id = uuid.uuid4().hex[:6].upper()
            self.reference_recu = f"{prefix}-{unique_id}"

        # 2. Utiliser une transaction pour garantir la cohérence des calculs
        with transaction.atomic():
            super().save(*args, **kwargs)
