from pyspark.sql import SparkSession, DataFrame

from Core.Configurations import AbstractConfig1
from Interpretors import AbstractQueryInterpreter


class DatabaseQueryInterpreter(AbstractQueryInterpreter):
    def __init__(self):
        super().__init__()
    def interpret(self, spark: SparkSession, config:AbstractConfig1) -> DataFrame:
        raise NotImplementedError("Sorry, interpret() method is not implemented")
        # master_data_frame = spark.table(self._containers[0]['name'])
        #
        # for join in self._joins:
        #     join_data_frame = spark.table(join['rightContainer'])
        #     master_data_frame = master_data_frame.join(join_data_frame, master_data_frame[
        #         join['leftContainer'] + "." + join['on']['leftField']] == join_data_frame[
        #                                                    join['rightContainer'] + "." + join['on']['rightField']])
        #
        # for predicate in self._predicates:
        #     if isinstance(predicate['value'], str):
        #         master_data_frame = master_data_frame.filter(
        #             col(predicate['field']) + " " + predicate['operator'] + " '" + predicate['value'] + "'")
        #     else:
        #         master_data_frame = master_data_frame.filter(
        #             col(predicate['field']) + " " + predicate['operator'] + " " + str(predicate['value']))
        #
        # if self._aggregations:
        #     agg_exprs = [expr(aggregation['function'] + "(" + aggregation['field'] + ")") for aggregation in
        #                  self._aggregations]
        #     master_data_frame = master_data_frame.groupBy(*[col(x['field']) for x in self._projections if
        #                                                     'count' not in x['field'] and 'avg' not in x['field']]).agg(
        #         *agg_exprs)
        #
        # for filter in self._filters:
        #     if isinstance(filter['value'], str):
        #         master_data_frame = master_data_frame.filter(
        #             col(filter['field']) + " " + filter['operator'] + " '" + filter['value'] + "'")
        #     else:
        #         master_data_frame = master_data_frame.filter(
        #             col(filter['field']) + " " + filter['operator'] + " " + filter['value'])
        #
        # for sort in self._sorts:
        #     master_data_frame = master_data_frame.sort(col(sort['field']), ascending=(sort['order'] == 'asc'))
        #
        # return master_data_frame.select([col(x['field']) for x in self._projections])
