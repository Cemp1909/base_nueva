import time, json, random, os
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_HOST", "mosquitto")
PORT   = int(os.getenv("MQTT_PORT", "1883"))
TOPIC  = os.getenv("MQTT_TOPIC", "tienda/visitas/telemetry")

# client_id único para evitar choques entre publisher1 y publisher2
client = mqtt.Client(client_id=f"publisher1-{random.randint(1000,9999)}")

# Reintentos para esperar a que Mosquitto esté listo
for i in range(10):
    try:
        client.connect(BROKER, PORT, 60)
        print("✅ Conectado al broker MQTT")
        break
    except Exception as e:
        print(f"Intento {i+1}/10: broker no disponible ({e}). Reintentando en 3s...")
        time.sleep(3)
else:
    raise SystemExit("❌ No fue posible conectarse al broker MQTT.")

while True:
    payload = {
        "visits": random.randint(1, 5),
        "source": random.choice(["instagram", "tiktok", "direct", "ads"])
    }
    client.publish(TOPIC, json.dumps(payload), qos=0, retain=False)
    print("publisher1 ->", payload)
    time.sleep(5)
