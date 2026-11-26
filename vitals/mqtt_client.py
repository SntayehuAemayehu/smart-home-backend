import json
import paho.mqtt.client as mqtt
from .models import VitalsReading

TOPIC_DATA = 'health/device1/data'
TOPIC_COMMAND = 'health/device1/command'

# Create a global client so we can use it in views
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("🔵 [DJANGO] Connected to MQTT Broker")
    client.subscribe(TOPIC_DATA)

def on_message(client, userdata, msg):
    if msg.topic == TOPIC_DATA:
        payload = json.loads(msg.payload.decode())
        print(f"📊 [DJANGO] Received data from hardware: {payload}")
        
        # Save to database
        VitalsReading.objects.create(
            device_id=payload['deviceId'],
            heart_rate=payload['heartRate'],
            temperature=payload['temperature']
        )
        
        # Automation Logic: If heart rate > 100, send ALARM command back to hardware
        if payload['heartRate'] > 100:
            command = json.dumps({"action": "ALARM_ON"})
            mqtt_client.publish(TOPIC_COMMAND, command)
            print("🚨 [DJANGO] Heart rate critical! Sent ALARM_ON to hardware.")

def start_mqtt():
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("broker.hivemq.com", 1883, 60)
    mqtt_client.loop_start() # Runs in background thread