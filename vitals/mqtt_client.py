import paho.mqtt.client as mqtt
import json
from .models import SmartHomeDevice

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_SENSOR = "ethio_home/sensor"
TOPIC_COMMAND = "ethio_home/command"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"🔵 [DJANGO] Connected to MQTT Broker (rc={reason_code})")
    client.subscribe(TOPIC_SENSOR)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"📊 [DJANGO] Received sensor data: {data}")
    except Exception as e:
        print(f"❌ MQTT error: {e}")

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def start_mqtt():
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.loop_start()
    print("🚀 MQTT background thread started")

def send_device_command(device_id: str, action: str):
    payload = json.dumps({"device": device_id, "action": action})
    
    # Publish the message to the MQTT Broker
    result = mqtt_client.publish(TOPIC_COMMAND, payload)
    print(f"📤 [DJANGO] Sent command: {payload} (Status: {result.rc})")
    
    # Try to update the database, but don't crash if it fails
    try:
        dev, created = SmartHomeDevice.objects.get_or_create(
            device_id=device_id,
            defaults={'name': 'Device', 'status': False}
        )
        dev.status = (action == "ON")
        dev.save()
    except Exception as e:
        print(f"⚠️ Database update skipped: {e}")