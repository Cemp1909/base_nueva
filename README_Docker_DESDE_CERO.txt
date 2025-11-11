PASOS DESDE CERO (Mac y Windows)

1) Instala Docker Desktop (Mac: DMG usual, Windows: requiere WSL2). Abre Docker Desktop y espera a que diga "Docker Engine is running".
2) Copia TODO el contenido de esta carpeta dentro de la raíz de tu proyecto Flask (donde está app.py).
   - Si tu app está en una subcarpeta, ajusta el 'build' del servicio 'webshop' en docker-compose.yml.
3) Crea la red externa (solo 1 vez):
   docker network create red-iot
4) Levanta los servicios:
   docker compose up -d --build
5) Verifica:
   docker ps
   - Deberías ver: mosquitto, portainer, influxdb, telegraf, grafana, publisher1, publisher2, postgres, webshop
6) Entra a tu app: http://localhost:5000
7) Suscríbete a MQTT (opción simple desde el contenedor):
   docker exec -it mosquitto mosquitto_sub -t 'tienda/+/telemetry' -v
8) Grafana: http://localhost:3000  (usuario admin / contraseña admin la primera vez; cámbiala)
9) Portainer: https://localhost:9443  (crea usuario admin, mínimo 12 caracteres)
10) Cuando hagas una compra en tu app Flask, publica un evento a 'tienda/ventas/telemetry' y lo verás en Telegraf/Influx/Grafana.

TROUBLESHOOTING RÁPIDO
- "network red-iot not found": ejecuta 'docker network create red-iot' y vuelve a levantar.
- "address already in use": cambia el puerto publicado (5000, 3000, 8086) si ya lo usas.
- Paquetes de Python fallan al compilar: asegúrate de tener 'libpq-dev' instalado (ya incluido) y usa psycopg2-binary.
