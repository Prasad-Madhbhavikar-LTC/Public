__all__ = [
    "CSVQueryInterpreter",
]

import logging
from abc import ABC, abstractmethod

from pyspark.sql import SparkSession, DataFrame

from Core.Configurations import AbstractConfig1

LOGGER = logging.getLogger(__name__)


class AbstractQueryInterpreter(ABC):
    def __init__(self):
        self._projections = []
        self._containers = []
        self._joins = []
        self._predicates = []
        self._aggregations = []
        self._filters = []
        self._sorts = []
        self._fields = {}

    @abstractmethod
    def interpret(self, spark: SparkSession, config: AbstractConfig1) -> DataFrame:
        raise NotImplementedError("Subclass must implement interpret() method")

    def load_query(self, raw_query_spec):
        # FIXME: Should load the query part from the Configurations ??
        pass

#
# import yaml
# from pyspark.sql import SparkSession
#
# # Initialize SparkSession
# spark = SparkSession.builder.getOrCreate()
#
# # Load YAML file
# with open('your_file.yaml', 'r') as file:
#     data = yaml.safe_load(file)
#
# # Initialize Query1 class
# query = Query1()
#
# # Add projections
# for projection in data.get('projections', []):
#     query.add_projection(projection)
#
# # Add containers
# for container in data.get('containers', []):
#     query.add_container(container)
#
# # Add joins
# for join in data.get('joins', []):
#     query.add_join(join)
#
# # Add predicates
# for predicate in data.get('predicates', []):
#     query.add_predicate(predicate)
#
# # Add aggregations
# for aggregation in data.get('aggregations', []):
#     query.add_aggregation(aggregation)
#
# # Add filters
# for filter in data.get('filters', []):
#     query.add_filter(filter)
#
# # Add sorts
# for sort in data.get('sorts', []):
#     query.add_sort(sort)
#
# # Build the query
# df = query.build_query(spark)
