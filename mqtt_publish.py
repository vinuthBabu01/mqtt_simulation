import time
import random
import paho.mqtt.client as mqtt

# MQTT Configuration
MQTT_BROKER = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
CLIENT_ID = "DiwhDggPKw08HiQnNTgcKR4"
USERNAME = "DiwhDggPKw08HiQnNTgcKR4"
PASSWORD = "LfNhVqPoPleK/IpRy3bieUQ/"
CHANNEL_ID = "2840278"
TOPIC = f"channels/{CHANNEL_ID}/publish"
LOG_FILE = "sensor_log.txt"
PUBLISH_INTERVAL = 15  # ThingSpeak allows updates every 15 seconds


def initialize_mqtt_client():
    client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client


def generate_sensor_data():
    return {
        "temperature": round(random.uniform(-50, 50), 2),
        "humidity": round(random.uniform(0, 100), 2),
        "co2": random.randint(300, 2000),
    }


def log_sensor_data(timestamp, data):
    with open(LOG_FILE, "a") as file:
        file.write(f"{timestamp},{data['temperature']},{data['humidity']},{data['co2']}\n")


def publish_sensor_data(client):
    data = generate_sensor_data()
    payload = f"field1={data['temperature']}&field2={data['humidity']}&field3={data['co2']}"
    
    if client.publish(TOPIC, payload)[0] == 0:
        print(f"✅ Sent: {payload}")
        log_sensor_data(time.strftime('%Y-%m-%d %H:%M:%S'), data)
    else:
        print("❌ Failed to send message")


def main():
    client = initialize_mqtt_client()
    print("🚀 Publishing sensor data to ThingSpeak...")
    time.sleep(5)
    
    while True:
        publish_sensor_data(client)
        time.sleep(PUBLISH_INTERVAL)


if __name__ == "__main__":
    main()
