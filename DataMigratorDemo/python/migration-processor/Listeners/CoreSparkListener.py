import logging
import time
from typing import Any

from Emmiters import AbstractEmitter

LOGGER = logging.getLogger(__name__)


class CustomSparkListener(SparkListener):
    def __init__(self, producer: AbstractEmitter):
        self.__producer = producer
        LOGGER.info("CustomSparkListener initialized.")

    def onJobEnd(self, job_end: Any):
        try:
            event = {
                "job_id": job_end.jobId(),
                "job_result": str(job_end.jobResult())
            }
            self.__producer.emit('JobEnd', event, int(time.time()))
            LOGGER.debug(f"Sent event 'JobEnd' to Kafka: {event}")
        except Exception as e:
            LOGGER.error(f"Failed to process 'JobEnd' event: {e}")

    def onStageCompleted(self, stage_completed: Any):
        try:
            stage_info = stage_completed.stageInfo()
            event = {
                "stage_id": stage_info.stageId(),
                "stage_name": stage_info.name(),
                "num_tasks": stage_info.numTasks(),
                "completion_time": stage_info.completionTime(),
                "failure_reason": stage_info.failureReason()
            }
            self.__producer.emit('StageCompleted', event, int(time.time()))
            LOGGER.debug(f"Sent event 'StageCompleted' to Kafka: {event}")
        except Exception as e:
            LOGGER.error(f"Failed to process 'StageCompleted' event: {e}")

    def onExecutorMetricsUpdate(self, executor_metrics_update: Any):
        try:
            for executor_id, executor_metrics in executor_metrics_update.executorUpdates().items():
                event = {
                    "executor_id": executor_id,
                    "metrics": executor_metrics
                }
                self.__producer.emit('ExecutorMetricsUpdate', event, int(time.time()))
                LOGGER.info(f"Sent event 'ExecutorMetricsUpdate' to Kafka: {event}")
        except Exception as e:
            LOGGER.error(f"Failed to process 'ExecutorMetricsUpdate' event: {e}")

    def on_spark_event(self, event_name: str, java_event: Any):
        self.__producer.emit(event_name, java_event, int(time.time()))

    def onApplicationEnd(self, application_end: Any):
        self.__producer.emit('applicationEnd', application_end, int(time.time()))

    def onApplicationStart(self, application_start: Any):
        self.__producer.emit('applicationStart', application_start, int(time.time()))

    def onBlockManagerRemoved(self, block_manager_removed: Any):
        self.__producer.emit('blockManagerRemoved', block_manager_removed, int(time.time()))

    def onBlockUpdated(self, block_updated: Any):
        self.__producer.emit('blockUpdated', block_updated, int(time.time()))

    def onEnvironmentUpdate(self, environment_update: Any):
        self.__producer.emit('environmentUpdate', environment_update, int(time.time()))

    def onExecutorAdded(self, executor_added: Any):
        self.__producer.emit('executorAdded', executor_added, int(time.time()))

    def onExecutorRemoved(self, executor_removed: Any):
        self.__producer.emit('executorRemoved', executor_removed, int(time.time()))

    def onJobStart(self, job_start: Any):
        self.__producer.emit('jobStart', job_start, int(time.time()))

    def onOtherEvent(self, other_event: Any):
        self.__producer.emit('otherEvent', other_event, int(time.time()))

    def onStageSubmitted(self, stage_submitted: Any):
        self.__producer.emit('stageSubmitted', stage_submitted, int(time.time()))

    def onTaskEnd(self, task_end: Any):
        self.__producer.emit('taskEnd', task_end, int(time.time()))

    def onTaskGettingResult(self, task_getting_result: Any):
        self.__producer.emit('taskGettingResult', task_getting_result, int(time.time()))

    def onTaskStart(self, task_start):
        self.__producer.emit('taskStart', task_start, int(time.time()))

    def onUnpersistRDD(self, unpersist_rdd: Any):
        self.__producer.emit('unpersistRDD', unpersist_rdd, int(time.time()))
