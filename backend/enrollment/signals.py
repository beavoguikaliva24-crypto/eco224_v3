from django.db.models.signals import post_save
from django.dispatch import receiver
from enrollment.models import Affectation
from billing.models import Paiement

@receiver(post_save, sender=Affectation)
def generer_paiement_automatique(sender, instance, created, **kwargs):
    """
    Dès qu'une Affectation est créée, on génère le dossier de Paiement associé.
    """
    if created:
        # On vérifie si un paiement n'existe pas déjà par sécurité
        if not Paiement.objects.filter(affectation=instance).exists():
            Paiement.objects.create(
                affectation=instance,
                reduction=0,  # Par défaut 0% de réduction
            )
            print(f"✅ Dossier de paiement généré pour l'élève {instance.eleve.nom}")