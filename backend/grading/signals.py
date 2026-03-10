from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Note
# NE PAS importer 'services' en haut du fichier

@receiver(post_save, sender=Note, dispatch_uid="update_bulletin_on_note_save")
def handle_note_save(sender, instance, **kwargs):
    """
    Déclenche la mise à jour des bulletins après la sauvegarde d'une note.
    """
    # On importe les services ICI, à l'intérieur de la fonction
    from .services import generer_et_sauvegarder_bulletin_periodique, generer_et_sauvegarder_bulletin_annuel
    
    affectation_id = instance.affectation.id
    periode_id = instance.periodicite.id

    print(f"SIGNAL: Mise à jour du bulletin périodique pour affectation {affectation_id}, période {periode_id}")
    generer_et_sauvegarder_bulletin_periodique(affectation_id, periode_id)

    print(f"SIGNAL: Mise à jour du bulletin annuel pour affectation {affectation_id}")
    generer_et_sauvegarder_bulletin_annuel(affectation_id)


@receiver(post_delete, sender=Note, dispatch_uid="update_bulletin_on_note_delete")
def handle_note_delete(sender, instance, **kwargs):
    """
    Déclenche la mise à jour des bulletins après la suppression d'une note.
    """
    # On importe les services ICI aussi
    from .services import generer_et_sauvegarder_bulletin_periodique, generer_et_sauvegarder_bulletin_annuel

    affectation_id = instance.affectation.id
    periode_id = instance.periodicite.id

    print(f"SIGNAL: Mise à jour (suppression) pour bulletin périodique, affectation {affectation_id}")
    generer_et_sauvegarder_bulletin_periodique(affectation_id, periode_id)

    print(f"SIGNAL: Mise à jour (suppression) pour bulletin annuel, affectation {affectation_id}")
    generer_et_sauvegarder_bulletin_annuel(affectation_id)