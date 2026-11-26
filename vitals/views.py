from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VitalsReading
from .mqtt_client import mqtt_client, TOPIC_COMMAND
import json

@api_view(['GET'])
def get_latest_vitals(request):
    # Get the last 10 readings
    readings = VitalsReading.objects.all().order_by('-timestamp')[:10]
    data = [{"heartRate": r.heart_rate, "temperature": r.temperature, "time": r.timestamp} for r in readings]
    return Response(data)

@api_view(['POST'])
def reset_alarm(request):
    # This is triggered by the React button
    command = json.dumps({"action": "ALARM_OFF"})
    mqtt_client.publish(TOPIC_COMMAND, command)
    return Response({"status": "Alarm reset command sent to hardware"})