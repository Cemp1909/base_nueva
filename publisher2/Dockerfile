FROM python:3.11-slim
RUN pip install paho-mqtt
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
