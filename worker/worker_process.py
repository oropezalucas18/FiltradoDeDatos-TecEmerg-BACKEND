import json
from app.application.process_message_usecase import ProcessMessageUseCase

def process_message(ch, method, properties, body):
    message = json.loads(body)

    usecase = ProcessMessageUseCase()
    usecase.execute(message)

    ch.basic_ack(delivery_tag=method.delivery_tag)
