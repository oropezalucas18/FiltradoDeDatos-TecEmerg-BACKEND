from app.infrastructure.firebase_client import firebase_db
from app.domain.entities.sensor_data import SensorData
from app.domain.ports.repository_port import RepositoryPort

class FirebaseRepository(RepositoryPort):

    def save(self, data: SensorData):
        """
        Guarda los datos en Firestore con la estructura:
        sensores/{tipo}/data/{auto_id}/valores
        """
        path = f"sensores/{data.tipo}/data"

        firebase_db.collection(path).add({
            "valores": data.valores,
            "timestamp": data.timestamp,
            "origen": data.origen,
            "procesado": data.procesado
        })

    def get_last(self, tipo: str, limit: int):
        path = f"sensores/{tipo}/data"

        docs = (
            firebase_db.collection(path)
            .order_by("timestamp")
            .limit(limit)
            .stream()
        )

        return [d.to_dict() for d in docs]
