from django.apps import AppConfig
import os

class VitalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vitals'

    def ready(self):
        # Prevents double startup during auto-reload
        if os.environ.get('RUN_MAIN') == 'true':
            from .mqtt_client import start_mqtt
            start_mqtt()