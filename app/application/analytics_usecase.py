import pandas as pd
from app.domain.ports.repository_port import RepositoryPort

class AnalyticsUseCase:

    def __init__(self, repo: RepositoryPort):
        self.repo = repo

    def basic_stats(self, tipo: str, limit: int = 200):
        data = self.repo.get_last(tipo, limit)
        if not data:
            return {}

        df = pd.DataFrame(data)

        # eliminamos campos no numéricos
        df = df.select_dtypes(include=["number"])

        if df.empty:
            return {}

        return df.describe().to_dict()

    def time_series(self, tipo: str, field: str, limit: int = 200):
        data = self.repo.get_last(tipo, limit)
        if not data:
            return []

        series = []
        for d in data:
            if field in d:
                series.append({
                    "timestamp": d.get("_received_at") or d.get("time"),
                    "valor": d[field]
                })

        return series
