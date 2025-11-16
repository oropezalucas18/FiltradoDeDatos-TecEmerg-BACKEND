import pandas as pd
from app.domain.ports.repository_port import RepositoryPort

class AnalyticsUseCase:

    def __init__(self, repo: RepositoryPort):
        self.repo = repo

    def basic_stats(self, tipo: str, limit: int = 200):
        """
        Devuelve estadísticas simples:
        - promedio
        - mínimo
        - máximo
        - desvío estándar
        """
        data = self.repo.get_last(tipo, limit)
        if not data:
            return {}

        df = pd.DataFrame([d["valores"] for d in data])

        stats = df.describe().to_dict()
        return stats

    def time_series(self, tipo: str, field: str, limit: int = 200):
        """
        Devuelve una serie temporal de un campo específico.
        Ejemplo: tendencia de CO2, ruido, etc.
        """
        data = self.repo.get_last(tipo, limit)
        if not data:
            return []

        records = []
        for d in data:
            valor = d["valores"].get(field)
            timestamp = d.get("timestamp")

            if valor is not None and timestamp:
                records.append({"timestamp": timestamp, "valor": valor})

        return records
