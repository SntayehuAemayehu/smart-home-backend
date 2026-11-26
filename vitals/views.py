from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VitalsReading
from .mqtt_client import send_command

@api_view(['GET'])
def get_latest_vitals(request):
    readings = VitalsReading.objects.all().order_by('-id')[:10]
    data = [{"heartRate": r.heart_rate, "temperature": r.temperature, "time": r.timestamp} for r in readings]
    return Response(data)

@api_view(['POST'])
def reset_alarm(request):
    send_command("ALARM_OFF")
    return Response({"status": "Alarm reset sent"})