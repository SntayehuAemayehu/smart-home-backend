import paho.mqtt.client as mqtt
import json
from .models import SmartHomeDevice

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_SENSOR = "ethio_home/sensor"
TOPIC_COMMAND = "ethio_home/command"

# This is used to receive data (leave it as is)
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

# --- NEW FORCE SEND FUNCTION ---
def send_device_command(device_id: str, action: str):
    payload = json.dumps({"device": device_id, "action": action})
    
    print(f"⏳ [DJANGO] Attempting to send command to HiveMQ...")
    
    try:
        # Create a brand new temporary client just for this one command
        temp_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        temp_client.connect(BROKER, PORT, 60)
        
        # Publish and wait for it to finish
        info = temp_client.publish(TOPIC_COMMAND, payload)
        info.wait_for_publish() 
        
        temp_client.disconnect()
        print(f"📤 [DJANGO] SUCCESS: Sent command: {payload}")
        
    except Exception as e:
        print(f"❌ [DJANGO] FAILED to send MQTT: {e}")
    
    # Try to update the database
    try:
        dev, created = SmartHomeDevice.objects.get_or_create(
            device_id=device_id,
            defaults={'name': 'Device', 'status': False}
        )
        dev.status = (action == "ON")
        dev.save()
    except Exception as e:
        print(f"⚠️ Database update skipped: {e}")