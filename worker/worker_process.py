import json
import sys
sys.path.append("/app")

from app.application.process_message_usecase import ProcessMessageUseCase
from app.adapters.output.rabbitmq_queue import RabbitMQQueue
from app.infrastructure.rabbitmq_client import get_rabbitmq_channel

def process_message(ch, method, properties, body):
    message = json.loads(body)
    usecase = ProcessMessageUseCase()
    usecase.execute(message)

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    channel = get_rabbitmq_channel()
    channel.queue_declare(queue="sensor_data", durable=True)

    print("🐇 Worker escuchando cola 'sensor_data'...")
    channel.basic_consume(queue="sensor_data", on_message_callback=process_message)
    channel.start_consuming()
