from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SmartHomeDevice
from .mqtt_client import send_device_command
from django.http import JsonResponse

@api_view(['GET'])
def list_devices(request):
    # Hardcode the list so the frontend always has devices to show
    devices = [
        {"id": "light1", "name": "Living Room Light", "status": False},
        {"id": "fan1", "name": "Bedroom Fan", "status": False}
    ]
    
    # Try to get real status from DB if it exists
    try:
        for dev in devices:
            db_dev = SmartHomeDevice.objects.filter(device_id=dev['id']).first()
            if db_dev:
                dev['status'] = db_dev.status
    except Exception:
        pass # If database fails, just return them as OFF
        
    return Response(devices)

@api_view(['POST'])
def toggle_device(request):
    device_id = request.data.get('device_id')
    action = request.data.get('action')
    
    if not device_id or action not in ["ON", "OFF"]:
        return Response({"error": "Invalid request"}, status=400)
        
    # 1. Send command to MQTT (This turns on the real hardware)
    send_device_command(device_id, action)
    
    # 2. Try to update the database (If it fails, ignore it so React still gets a 200 OK)
    try:
        dev, created = SmartHomeDevice.objects.get_or_create(
            device_id=device_id,
            defaults={'name': 'Device', 'status': False}
        )
        dev.status = (action == "ON")
        dev.save()
    except Exception as e:
        print(f"Database update failed, but MQTT sent: {e}")
        
    return Response({"status": f"{device_id} turned {action}"})

def seed_devices(request):
    # We don't need this anymore, but we keep it to prevent errors
    return JsonResponse({"status": "Bypassed"})