from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import WaterReading
from .mqtt_client import send_command

@api_view(['GET'])
def get_latest_readings(request):
    readings = WaterReading.objects.all().order_by('-id')[:10]
    data = [{"turbidity": r.turbidity, "ph": r.ph, "time": r.timestamp} for r in readings]
    return Response(data)

@api_view(['POST'])
def dispatch_maintenance(request):
    send_command("DISPATCH_MAINTENANCE")
    return Response({"status": "Maintenance dispatched to field team"})