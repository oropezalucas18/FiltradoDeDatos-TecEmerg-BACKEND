import pika
from app.infrastructure.config import settings

def _create_connection():
    try:
        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USER,
            settings.RABBITMQ_PASS
        )

        params = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=5672,
            credentials=credentials,
            heartbeat=60,
            blocked_connection_timeout=300
        )

        return pika.BlockingConnection(params)

    except Exception as e:
        print("❌ Error conectando a RabbitMQ:", e)
        return None


# =======================================
# 🔹 Crear conexión global para la API
# =======================================
connection = _create_connection()
channel = None

if connection:
    try:
        channel = connection.channel()
        channel.queue_declare(
            queue=settings.RABBITMQ_QUEUE,
            durable=True
        )
        print("✔ RabbitMQ inicializado desde API")
    except Exception as e:
        print("❌ Error creando canal RabbitMQ:", e)
