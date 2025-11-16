from abc import ABC, abstractmethod
from typing import Callable, Dict, Any

class QueuePort(ABC):

    @abstractmethod
    def publish(self, message: Dict[str, Any]):
        """ Publica un mensaje en la cola """
        pass

    @abstractmethod
    def consume(self, callback: Callable):
        """ Consume mensajes, ejecutando un callback por cada uno """
        pass
