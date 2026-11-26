
from django.db import models

class SmartHomeDevice(models.Model):
    name = models.CharField(max_length=50)          # e.g. "Living Room Light"
    device_id = models.CharField(max_length=50)     # e.g. "light1"
    status = models.BooleanField(default=False)     # True = ON, False = OFF
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}: {'ON' if self.status else 'OFF'}"