import time, json, random, os
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_HOST", "mosquitto")
PORT   = int(os.getenv("MQTT_PORT", "1883"))
TOPIC  = os.getenv("MQTT_TOPIC", "tienda/operacion/telemetry")

client = mqtt.Client(client_id=f"publisher2-{random.randint(1000,9999)}")

# Espera a que el broker esté listo (hasta 10 intentos)
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

# Publica datos cada 5 segundos
while True:
    payload = {
        "carts_active": random.randint(0, 12),
        "api_latency_ms": round(random.uniform(80, 300), 1)
    }
    client.publish(TOPIC, json.dumps(payload))
    print("publisher2 ->", payload)
    time.sleep(5)
