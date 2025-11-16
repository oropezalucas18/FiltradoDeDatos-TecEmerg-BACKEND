from pyspark.sql import SparkSession
from app.domain.ports.file_parser_port import FileParserPort
import pandas as pd
import tempfile
import os

class SparkFileParser(FileParserPort):

    def __init__(self):
        """
        Inicializa Spark en modo local.
        Si más adelante usas cluster (YARN, Kubernetes),
        solo cambias las configs aquí.
        """
        self.spark = SparkSession.builder \
            .appName("GAMC-SparkParser") \
            .master("local[*]") \
            .config("spark.driver.memory", "2g") \
            .config("spark.executor.memory", "2g") \
            .config("spark.sql.shuffle.partitions", "8") \
            .getOrCreate()

    def parse(self, file):
        """
        Lee TXT, CSV o XLSX usando Spark.
        Devuelve un Pandas DataFrame (porque tu sistema usa Pandas internamente).
        """

        filename = file.filename.lower()

        # Spark no puede leer directamente un buffer, así que lo guardamos temporalmente
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        try:
            # =============================
            # LECTURA CON SPARK
            # =============================

            if filename.endswith(".csv") or filename.endswith(".txt"):
                df_spark = self.spark.read.csv(tmp_path, header=True, inferSchema=True)

            elif filename.endswith(".xlsx"):
                # Spark no puede leer Excel directamente → lo convertimos con Pandas
                temp_df = pd.read_excel(tmp_path)
                # Subimos a Spark
                df_spark = self.spark.createDataFrame(temp_df)

            else:
                raise Exception("Formato no soportado para Spark")

            # Convertimos Spark → Pandas
            df_pandas = df_spark.toPandas()
            return df_pandas

        finally:
            # Limpieza del archivo temporal
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
