from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from .models import LogAction, Notification
from .middleware import get_current_user
# Assurez-vous que votre modèle User est importé si nécessaire
# from django.contrib.auth import get_user_model
# User = get_user_model()

from django.contrib.admin.models import LogEntry

User = get_user_model()

# 1. Journalisation de la connexion
@receiver(user_logged_in, dispatch_uid="log_login_unique_id")
def log_login(sender, request, user, **kwargs):
    """
    Enregistre une action de connexion réussie.
    """
    LogAction.objects.create(
        utilisateur=user,
        action='LOGIN',
        table_nom=user.__class__.__name__,
        description=f"Connexion de l'utilisateur : {user.get_full_name() if hasattr(user, 'get_full_name') else user.username}",
        adresse_ip=request.META.get('REMOTE_ADDR')
    )

# 2. Journalisation de la déconnexion
@receiver(user_logged_out, dispatch_uid="log_logout_unique_id")
def log_logout(sender, request, user, **kwargs):
    """
    Enregistre une action de déconnexion.
    """
    if user:
        LogAction.objects.create(
            utilisateur=user,
            action='LOGOUT',
            table_nom=user.__class__.__name__,
            description=f"Déconnexion de l'utilisateur : {user.get_full_name() if hasattr(user, 'get_full_name') else user.username}",
            adresse_ip=request.META.get('REMOTE_ADDR')
        )

# 3. Journalisation des créations et mises à jour
@receiver(post_save, dispatch_uid="log_save_unique_id")
def log_save(sender, instance, created, **kwargs):
    """
    Enregistre une action de création ou de mise à jour sur n'importe quel modèle,
    en ignorant les modèles internes ou de log pour éviter le bruit et les boucles.
    """
    # Liste des modèles dont les modifications ne doivent pas être journalisées.
    ignored_models = (LogAction, Notification, LogEntry, Session)
    if sender in ignored_models:
        return
        
    # Ignorer les mises à jour sur le modèle User (pour éviter de logger le `last_login`)
    if sender == User and not created:
        return

    action_type = 'CREATE' if created else 'UPDATE'
    current_user = get_current_user()

    LogAction.objects.create(
        utilisateur=current_user if current_user and current_user.is_authenticated else None,
        action=action_type,
        table_nom=sender.__name__,
        description=f"{action_type} effectuée sur l'objet : {instance}"
    )

# 4. Journalisation des suppressions
@receiver(post_delete, dispatch_uid="log_delete_unique_id")
def log_delete(sender, instance, **kwargs):
    """
    Enregistre une action de suppression sur n'importe quel modèle,
    en ignorant les modèles de log.
    """
    ignored_models = (LogAction, Notification, LogEntry, Session)
    if sender in ignored_models:
        return
        
    current_user = get_current_user()

    LogAction.objects.create(
        utilisateur=current_user if current_user and current_user.is_authenticated else None,
        action='DELETE',
        table_nom=sender.__name__,
        description=f"SUPPRESSION définitive de l'objet : {instance}"
    )