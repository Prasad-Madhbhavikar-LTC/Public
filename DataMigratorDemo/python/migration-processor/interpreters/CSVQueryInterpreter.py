import logging

from pyspark.sql import SparkSession, DataFrame

from core.configurations.connectors import FileSystemConfig
from interpreters import AbstractQueryInterpreter

LOGGER = logging.getLogger(__name__)
class CSVQueryInterpreter(AbstractQueryInterpreter):
    def __init__(self):
        super().__init__()

    def interpret(self, spark: SparkSession, config: FileSystemConfig) -> DataFrame:
        return spark.read.csv(config.source_path, header=True, inferSchema=True)

