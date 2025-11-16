import pandas as pd
import numpy as np

class CleanerService:

    @staticmethod
    def clean(df: pd.DataFrame):
        """
        Limpieza general:
        - Elimina duplicados
        - Reemplaza NaN por None
        """
        df = df.drop_duplicates()
        df = df.replace({np.nan: None})
        return df

    @staticmethod
    def normalize(df: pd.DataFrame):
        """
        Normalización:
        - Convierte columnas numéricas a float
        - Mantiene timestamp intacto
        """
        for col in df.columns:
            if col != "timestamp":
                try:
                    df[col] = pd.to_numeric(df[col], errors="ignore")
                except:
                    pass
        return df
