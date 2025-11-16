from app.domain.ports.repository_port import RepositoryPort

class QueryUseCase:

    def __init__(self, repo: RepositoryPort):
        self.repo = repo

    def get_last_records(self, tipo: str, limit: int = 50):
        """
        Retorna los últimos N registros de un sensor específico.
        Se usa para dashboards, gráficos y vista rápida.
        """
        return self.repo.get_last(tipo, limit)
