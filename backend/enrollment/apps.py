from django.apps import AppConfig


class EnrollmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'enrollment'

    def ready(self):
        # Cette ligne importe les signals dès que l'application est prête
        import enrollment.signals