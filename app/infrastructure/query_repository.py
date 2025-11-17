from app.domain.ports.repository_port import RepositoryPort

class QueryRepository(RepositoryPort):

    def get_last(self, tipo: str, limit: int = 50):
        # TEMPORAL: devuelve datos falsos hasta conectar con la BD real
        return [
            {"value": 100, "timestamp": "2025-01-01T00:00:00Z"},
            {"value": 200, "timestamp": "2025-01-01T00:01:00Z"},
        ][:limit]
