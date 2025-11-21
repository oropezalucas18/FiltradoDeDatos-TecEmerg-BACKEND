from app.infrastructure.firebase_client import firebase_db, get_db
from app.domain.ports.repository_port import RepositoryPort

class FirebaseRepository(RepositoryPort):

    COLLECTION_ROOT = "sensores"

    def _normalize_tipo(self, tipo: str):
        tipo = tipo.lower()
        map_tipos = {
            "co2": "air_quality",
            "sonido": "sound",
            "soterrado": "water"
        }
        return map_tipos.get(tipo, tipo)

    SENSOR_MAP = {
        "CO2": "air_quality",
        "SONIDO": "sound",
        "SOTERRADO": "water"
    }

    def get_last(self, tipo: str, limit: int):

        db = get_db()
        if db is None:
            raise RuntimeError("Firebase DB not initialized")

        tipo_normalizado = tipo.strip().upper()

        if tipo_normalizado not in self.SENSOR_MAP:
            raise ValueError(f"Tipo de sensor inválido: {tipo}")

        firestore_tipo = self.SENSOR_MAP[tipo_normalizado]
        path = f"sensores/{firestore_tipo}/lecturas"

        docs = (
            db.collection(path)
            .order_by("time")
            .limit(limit)
            .stream()
        )

        return [d.to_dict() for d in docs]

    def save(self, data: dict):
        """
        NO se usa porque el nuevo ETL escribe directamente en Firestore.
        Pero lo dejamos por compatibilidad.
        """
        tipo_norm = self._normalize_tipo(data.get("tipo", ""))
        firebase_db.collection(self.COLLECTION_ROOT)\
            .document(tipo_norm)\
            .collection("lecturas")\
            .add(data)
