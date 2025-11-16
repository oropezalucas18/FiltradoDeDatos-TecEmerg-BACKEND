from abc import ABC, abstractmethod
import pandas as pd

class FileParserPort(ABC):

    @abstractmethod
    def parse(self, file) -> pd.DataFrame:
        """
        Debe devolver un DataFrame con los datos del sensor.
        """
        pass
