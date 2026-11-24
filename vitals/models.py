from django.db import models

class WaterReading(models.Model):
    device_id = models.CharField(max_length=50)
    turbidity = models.FloatField()
    ph = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_id} - Turbidity: {self.turbidity}, pH: {self.ph}"