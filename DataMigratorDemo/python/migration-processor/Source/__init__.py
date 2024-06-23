__all__ = [
    'SourceFactory'
]

import logging
from abc import ABC, abstractmethod
from idlelib.query import Query

from pykwalify.core import Core
from pyspark import SparkContext
from pyspark.sql import DataFrame

from core import Type

logging.getLogger(__name__).addHandler(logging.NullHandler())


class AbstractSource(ABC):
    def __init__(self, spark_context: SparkContext, source_type: Type) -> None:
        super().__init__()
        self._spark_context = spark_context
        self._source_type = source_type

    @abstractmethod
    def read(self, query: Query):
        raise NotImplementedError("Subclasses must implement read method")


class Query1:
    def __init__(self):
        self._projections = []
        self._containers = []
        self._joins = []
        self._predicates = []
        self._aggregations = []
        self._filters = []
        self._sorts = []

    def add_projection(self, projection):
        self._projections.append(projection)

    def add_container(self, container):
        self._containers.append(container)

    def add_join(self, join):
        self._joins.append(join)

    def add_predicate(self, predicate):
        self._predicates.append(predicate)

    def add_aggregation(self, aggregation):
        self._aggregations.append(aggregation)

    def add_filter(self, filter):
        self._filters.append(filter)

    def add_sort(self, sort):
        self._sorts.append(sort)

    def validate_schema(self):
        core = Core(source_file=self.yaml_file, schema_files=[self.schema_file])
        core.validate(raise_exception=True)
        self.query_data = core.source
        self.logger.info('Schema validation successful')

    # def build_query(self):
    #     # Start building the query
    #     query = "SELECT "
    #
    #     # Add the projections
    #     projections = ', '.join([p['field'] for p in self.query_data['projections']])
    #     query += projections
    #
    #     # Add the containers
    #     containers = ', '.join([c['name'] for c in self.query_data['containers']])
    #     query += " FROM " + containers
    #
    #     # Add the joins
    #     for join in self.query_data['joins']:
    #         query += " JOIN " + join['container2']
    #         query += " ON " + join['container1'] + "." + join['on']['field1']
    #         query += " = " + join['container2'] + "." + join['on']['field2']
    #
    #     # Add the predicates
    #     if self.query_data['predicates']:
    #         predicates = ' AND '.join(
    #             [p['field'] + " " + p['operator'] + " " + str(p['value']) for p in self.query_data['predicates']])
    #         query += " WHERE " + predicates
    #
    #     # Add the aggregations
    #     if self.query_data['aggregations']:
    #         aggregations = ', '.join([a['function'] + "(" + a['field'] + ")" for a in self.query_data['aggregations']])
    #         query += ", " + aggregations
    #
    #     # Add the filters
    #     if self.query_data['filters']:
    #         filters = ' AND '.join(
    #             [f['field'] + " " + f['operator'] + " " + f['value'] for f in self.query_data['filters']])
    #         query += " HAVING " + filters
    #
    #     # Add the sorts
    #     if self.query_data['sorts']:
    #         sorts = ', '.join([s['field'] + " " + s['order'] for s in self.query_data['sorts']])
    #         query += " ORDER BY " + sorts
    #
    #     self.logger.info('Built query: %s', query)
    #     return query

    def build_query(self, spark_context: SparkContext) -> DataFrame:
        master_data_frame = spark.table(self._containers[0])

        # Add the joins
        for join in self.query_data['joins']:
            join_data_frame = spark.table(join['container2'])
            master_data_frame = master_data_frame.join(join_data_frame, master_data_frame[
                join['container1'] + "." + join['on']['field1']] == join_data_frame[
                                                           join['container2'] + "." + join['on']['field2']])

        # Add the predicates
        for predicate in self.query_data['predicates']:
            master_data_frame = master_data_frame.filter(
                col(predicate['field']) + " " + predicate['operator'] + " " + str(predicate['value']))

        # Add the aggregations
        for aggregation in self.query_data['aggregations']:
            master_data_frame = master_data_frame.groupBy(aggregation['field']).agg(
                expr(aggregation['function'] + "(" + aggregation['field'] + ")"))

        # Add the filters
        for filter in self.query_data['filters']:
            master_data_frame = master_data_frame.filter(
                col(filter['field']) + " " + filter['operator'] + " " + filter['value'])

        # Add the sorts
        for sort in self.query_data['sorts']:
            master_data_frame = master_data_frame.sort(col(sort['field']), ascending=(sort['order'] == 'asc'))

        self.logger.info('Built query')
        return master_data_frame

# import yaml
#
# with open('query.yaml', 'r') as file:
#     query_data = yaml.safe_load(file)
#
# query = Query()
# for projection in query_data['projections']:
#     query.add_projection(projection)
# for container in query_data['containers']:
#     query.add_container(container)
# for join in query_data['joins']:
#     query.add_join((join['container1'], join['container2'], join['condition']))
# for predicate in query_data['predicates']:
#     query.add_predicate((predicate['field'], predicate['operator'], predicate['value']))
# for sort in query_data['sorts']:
#     query.add_sort((sort['field'], sort['order']))
#
# query.execute()
