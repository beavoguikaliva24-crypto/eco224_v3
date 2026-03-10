from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import LogAction, Notification

# 1. Connexion
@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    LogAction.objects.create(
        utilisateur=user,
        action='LOGIN',
        table_nom='User',
        description=f"Connexion de l'utilisateur : {user.get_full_name()} ({user.contact})",
        adresse_ip=request.META.get('REMOTE_ADDR')
    )

# 2. Déconnexion
@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    if user:
        LogAction.objects.create(
            utilisateur=user,
            action='LOGOUT',
            table_nom='User',
            description=f"Déconnexion de l'utilisateur : {user.get_full_name()} ({user.contact})",
            adresse_ip=request.META.get('REMOTE_ADDR')
        )

# 3. Création et Mise à jour (post_save)
@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    # Important : Ne pas logger les logs eux-mêmes
    if sender in [LogAction, Notification]:
        return

    action_type = 'CREATE' if created else 'UPDATE'
    LogAction.objects.create(
        action=action_type,
        table_nom=sender.__name__,
        description=f"{action_type} effectuée sur l'objet : {instance}"
    )

# 4. Suppression (post_delete)
@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender in [LogAction, Notification]:
        return

    LogAction.objects.create(
        action='DELETE',
        table_nom=sender.__name__,
        description=f"SUPPRESSION définitive de l'objet : {instance}"
    )