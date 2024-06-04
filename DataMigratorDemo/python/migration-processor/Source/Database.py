import logging
from pyspark import SparkContext
from pyspark.sql import DataFrame

from Source import AbstractSource, Type, Query

LOGGER = logging.getLogger(__name__)


class DataSource(AbstractSource):
    def __init__(self, spark_context: SparkContext, source_type: Type, url: str, user_name: str, password: str,
                 schema_name: str):
        super().__init__(spark_context, source_type)
        self.__url = url
        self.__user_name = user_name
        self.__password = password
        self.__schema_name = schema_name

    def read(self, query:Query) -> DataFrame:
        pass
