from django.apps import AppConfig

class VitalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vitals'

    def ready(self):
        from .mqtt_client import start_mqtt
        start_mqtt()