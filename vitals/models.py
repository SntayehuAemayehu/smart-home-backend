from django.db import models

class VitalsReading(models.Model):
    device_id = models.CharField(max_length=50)
    heart_rate = models.IntegerField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_id} - HR: {self.heart_rate}, Temp: {self.temperature}"