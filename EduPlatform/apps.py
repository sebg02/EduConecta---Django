from django.apps import AppConfig


class EduplatformConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EduPlatform'

    def ready(self):
        import EduPlatform.signals