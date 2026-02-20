from django.apps import AppConfig


class MonAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mon_app'

    def ready(self):
        # Import des signaux pour qu'ils soient chargés au démarrage
        import mon_app.signals
