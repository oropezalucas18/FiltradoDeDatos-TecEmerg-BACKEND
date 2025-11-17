import pika
import json
from app.infrastructure.config import settings


class RabbitMQQueue:

    def __init__(self):
        self.host = settings.RABBITMQ_HOST
        self.user = settings.RABBITMQ_USER
        self.password = settings.RABBITMQ_PASS
        self.queue_name = settings.RABBITMQ_QUEUE

    # ============================
    # ENVIAR MENSAJES (API)
    # ============================
    def publish(self, message: dict):

            # 🔥 Conexión robusta para Docker
            credentials = pika.PlainCredentials(self.user, self.password)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    credentials=credentials,
                    heartbeat=30,
                    blocked_connection_timeout=600
                )
            )

            channel = connection.channel()

            # 🔥 Cola durable (no se pierde si se reinicia RabbitMQ)
            channel.queue_declare(
                queue=self.queue_name,
                durable=True
            )

            # 🔥 Publicación persistente
            channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2  # persistente
                )
            )

            print(f"📤 [RabbitMQ] Mensaje enviado a cola '{self.queue_name}'")

            connection.close()

    # ============================
    # CONSUMIR MENSAJES (WORKER)
    # ============================
    def start_worker(self, callback):
        credentials = pika.PlainCredentials(self.user, self.password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, credentials=credentials)
        )
        channel = connection.channel()

        channel.queue_declare(queue=self.queue_name, durable=True)

        print("📥 Worker escuchando cola RabbitMQ...")

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback
        )

        channel.start_consuming()
