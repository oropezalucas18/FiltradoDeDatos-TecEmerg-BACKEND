from app.domain.services.sensor_validator import SensorValidator
from app.domain.ports.file_parser_port import FileParserPort
from app.domain.ports.queue_port import QueuePort

class IngestUseCase:

    def __init__(self, parser: FileParserPort, queue: QueuePort):
        self.parser = parser
        self.queue = queue

    # ==============================
    # EXTRAER FILAS DEL ARCHIVO
    # ==============================
    def extract_rows(self, file):
        """
        Recibe el archivo enviado por FastAPI,
        lo convierte en un DataFrame usando un parser (Pandas o Spark),
        luego devuelve la lista de registros como diccionarios.
        """
        df = self.parser.parse(file)
        return df.to_dict(orient="records")

    # ==============================
    # PUBLICAR EN RABBITMQ
    # ==============================
    def publish_to_queue(self, tipo: str, rows, user_email: str):
        """
        Envía a RabbitMQ el mensaje con los datos crudos del archivo.
        El worker hará la limpieza, validación y guardado.
        """

        message = {
            "tipo": tipo,
            "rows": rows,
            "origen": "archivo",
            "subido_por": user_email
        }

        self.queue.publish(message)
        return True
