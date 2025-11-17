import json
import pyspark.sql.functions as F
from pyspark.sql import SparkSession

class SparkFileParser:

    def __init__(self):
        self.spark = SparkSession.builder.appName("FileParser").getOrCreate()

    def parse_file(self, file_path: str):
        df = self.spark.read.json(file_path)
        return df.toJSON().collect()
