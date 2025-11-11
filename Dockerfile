# Dockerfile genérico para una app Flask existente.
FROM python:3.11-slim
WORKDIR /app

# Instala dependencias del sistema si las necesitas (psycopg2, etc.)
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia TODO tu proyecto. Ajusta si necesitas excluir cosas con .dockerignore
COPY . .

# Variables comunes de Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expone el puerto interno
EXPOSE 5000

# Arranca Flask
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
