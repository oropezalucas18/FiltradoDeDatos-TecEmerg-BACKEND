from abc import ABC, abstractmethod
from typing import List, Dict, Any

class RepositoryPort(ABC):

    @abstractmethod
    def save(self, data):
        """ Guarda un registro procesado en la base """
        pass

    @abstractmethod
    def get_last(self, tipo: str, limit: int) -> List[Dict[str, Any]]:
        """ Obtiene los últimos registros de un sensor """
        pass
