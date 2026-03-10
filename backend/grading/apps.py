from django.apps import AppConfig

class GradingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'grading'

    def ready(self):
        """
        Cette méthode est appelée lorsque l'application est prête.
        C'est l'endroit recommandé pour importer les signaux.
        """
        import grading.signals