import json
from app.domain.ports.queue_port import QueuePort
from app.infrastructure.rabbitmq_client import channel, connection
from app.infrastructure.config import settings

class RabbitMQQueue(QueuePort):

    QUEUE_NAME = settings.RABBITMQ_QUEUE

    def publish(self, message: dict):
        """
        Publica mensajes hacia RabbitMQ.
        Si la conexión murió, no rompe el sistema (solo loguea).
        """
        if not connection or not channel:
            print("❌ No hay conexión a RabbitMQ. Mensaje NO enviado.")
            return

        try:
            channel.basic_publish(
                exchange="",
                routing_key=self.QUEUE_NAME,
                body=json.dumps(message),
                properties=None
            )
            print(f"📤 Mensaje enviado a cola '{self.QUEUE_NAME}'")

        except Exception as e:
            print("❌ Error publicando mensaje en RabbitMQ:", e)

    def consume(self, callback):
        """
        Este método no lo usa FastAPI.
        Solo está aquí por interfaz hexagonal.
        El worker usa su propia conexión independiente.
        """
        print("⚠ RabbitMQQueue.consume() no debe usarse desde API.")
        pass
