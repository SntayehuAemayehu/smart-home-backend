
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SmartHomeDevice
from .mqtt_client import send_device_command

@api_view(['GET'])
def list_devices(request):
    devices = SmartHomeDevice.objects.all()
    data = [{"id": d.device_id, "name": d.name, "status": d.status} for d in devices]
    return Response(data)

@api_view(['POST'])
def toggle_device(request):
    device_id = request.data.get('device_id')
    action = request.data.get('action')  # "ON" or "OFF"
    
    if not device_id or action not in ["ON", "OFF"]:
        return Response({"error": "Invalid request"}, status=400)
        
    send_device_command(device_id, action)
    return Response({"status": f"{device_id} turned {action}"})


def seed_devices(request):
    # Create devices if they don't exist
    SmartHomeDevice.objects.get_or_create(
        device_id="light1", 
        defaults={"name": "Living Room Light", "status": False}
    )
    SmartHomeDevice.objects.get_or_create(
        device_id="fan1", 
        defaults={"name": "Bedroom Fan", "status": False}
    )
    return JsonResponse({"status": "Database seeded successfully!"})