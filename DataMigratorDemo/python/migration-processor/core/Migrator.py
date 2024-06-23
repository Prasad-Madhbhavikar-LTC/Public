import logging

from pyspark.sql import DataFrame, SparkSession
from core.configurations import ConfigFactory, AbstractConfig1

LOGGER = logging.getLogger(__name__)
class Migrator(object):
    def __init__(self, source_config_path: str, target_config_path: str, job_config_path: str):
        self.config: AbstractConfig1 = ConfigFactory.read_config(source_config_path, job_config_path, target_config_path)
        self.spark : SparkSession = SparkSession.builder.appName(self.config._job_name).getOrCreate()


    def read(self) -> DataFrame:
        pass

    def transform(self) -> DataFrame:
        pass

    def write(self) -> bool:
        pass

    def validate(self) -> bool | {}:
        pass
