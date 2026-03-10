from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Note
from .services import generer_et_sauvegarder_bulletin_periodique, generer_et_sauvegarder_bulletin_annuel

@receiver(post_save, sender=Note, dispatch_uid="update_bulletin_on_note_save")
def handle_note_save(sender, instance, **kwargs):
    """
    Cette fonction est appelée chaque fois qu'une note est créée ou modifiée.
    Elle déclenche la mise à jour du bulletin périodique et annuel de l'élève concerné.
    """
    affectation_id = instance.affectation.id
    periode_id = instance.periodicite.id

    # On met à jour le bulletin de la période concernée
    print(f"Mise à jour du bulletin périodique pour l'affectation {affectation_id}, période {periode_id}")
    generer_et_sauvegarder_bulletin_periodique(affectation_id, periode_id)

    # On met également à jour le bulletin annuel
    print(f"Mise à jour du bulletin annuel pour l'affectation {affectation_id}")
    generer_et_sauvegarder_bulletin_annuel(affectation_id)


@receiver(post_delete, sender=Note, dispatch_uid="update_bulletin_on_note_delete")
def handle_note_delete(sender, instance, **kwargs):
    """
    Cette fonction est appelée chaque fois qu'une note est supprimée.
    Elle déclenche la mise à jour pour recalculer les moyennes sans cette note.
    """
    affectation_id = instance.affectation.id
    periode_id = instance.periodicite.id

    # On met à jour le bulletin de la période concernée
    print(f"Mise à jour du bulletin périodique suite à suppression de note pour l'affectation {affectation_id}, période {periode_id}")
    generer_et_sauvegarder_bulletin_periodique(affectation_id, periode_id)

    # On met également à jour le bulletin annuel
    print(f"Mise à jour du bulletin annuel suite à suppression de note pour l'affectation {affectation_id}")
    generer_et_sauvegarder_bulletin_annuel(affectation_id)