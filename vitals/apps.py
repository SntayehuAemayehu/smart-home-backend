from django.apps import AppConfig
import os
import sys

class VitalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vitals'

    def ready(self):
        # 1. Start MQTT
        if os.environ.get('RUN_MAIN') == 'true' or 'gunicorn' in sys.argv[0]:
            from .mqtt_client import start_mqtt
            start_mqtt()

        # 2. Auto-create devices when the server starts
        try:
            from .models import SmartHomeDevice
            # This safely checks if the table exists yet before adding data
            if not SmartHomeDevice.objects.filter(device_id='light1').exists():
                SmartHomeDevice.objects.create(name="Living Room Light", device_id="light1")
            if not SmartHomeDevice.objects.filter(device_id='fan1').exists():
                SmartHomeDevice.objects.create(name="Bedroom Fan", device_id="fan1")
        except Exception:
            # Ignore errors during the very first migration build
            pass