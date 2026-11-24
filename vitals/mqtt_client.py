import paho.mqtt.client as mqtt
import json
from .models import WaterReading

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_SENSOR = "water_project/device1/sensor"
TOPIC_COMMAND = "water_project/device1/command"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"🔵 [DJANGO] Connected to MQTT Broker (rc={reason_code})")
    client.subscribe(TOPIC_SENSOR)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"📊 Received: {data}")
        
        WaterReading.objects.create(
            device_id=str(data.get('deviceId', 'unknown')),
            turbidity=float(data.get('turbidity', 0)),
            ph=float(data.get('ph', 7))
        )
        print("💾 Saved to SQLite!")
    except Exception as e:
        print(f"❌ Error: {e}")

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def start_mqtt():
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.loop_start()
    print("🚀 MQTT started")

def send_command(action: str):
    payload = json.dumps({"action": action})
    mqtt_client.publish(TOPIC_COMMAND, payload)
    print(f"📤 Sent command: {payload}")