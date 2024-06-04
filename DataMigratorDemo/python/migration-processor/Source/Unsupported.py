import logging

from pyspark import SparkContext

from Source import AbstractSource, Type, Query

LOGGER = logging.getLogger(__name__)


class NOP(AbstractSource):
    def __init__(self, spark_context: SparkContext, source_type: Type):
        super().__init__(spark_context, source_type)

    def read(self, query: Query):
        LOGGER.warning("NOP Source selected, will perform nothing and will return nothing")
        raise ValueError(f"Unsupported source type: {super()._source_type}")
