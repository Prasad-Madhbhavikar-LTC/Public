import json
import time
import logging
from typing import Any

from pyspark.streaming.listener import StreamingListener

from Emmiters import AbstractEmitter

LOGGER = logging.getLogger(__name__)


class BatchStreamingListener(StreamingListener):
    def __init__(self, producer: AbstractEmitter):
        super().__init__()
        self.__emitter = producer
        LOGGER.info("BatchStreamingListener initialized.")

    def onBatchCompleted(self, batch_completed: Any) -> None:
        try:
            batch_info = batch_completed.batchInfo()
            event = {
                "batchTime": batch_info.batchTime().toString(),
                "totalDelay": batch_info.totalDelay().get(),
                "numRecords": batch_info.numRecords(),
                "processingDelay": batch_info.processingDelay().get(),
                "schedulingDelay": batch_info.schedulingDelay().get(),
            }
            self.__emitter.emit('BatchCompleted', event, int(time.time()))
            LOGGER.info(f"Sent event 'BatchCompleted' to Kafka: {event}")
        except Exception as e:
            LOGGER.error(f"Failed to process 'BatchCompleted' event: {e}")

    def onStreamingStarted(self, streaming_started: Any) -> None:
        self.__emitter.emit('StreamingStarted', streaming_started, int(time.time()))

    def onReceiverStarted(self, receiver_started: Any) -> None:
        self.__emitter.emit('ReceiverStarted', receiver_started, int(time.time()))

    def onReceiverError(self, receiver_error: Any) -> None:
        self.__emitter.emit('ReceiverError', receiver_error, int(time.time()))

    def onReceiverStopped(self, receiver_stopped: Any) -> None:
        self.__emitter.emit('ReceiverStopped', receiver_stopped, int(time.time()))

    def onBatchSubmitted(self, batch_submitted: Any) -> None:
        self.__emitter.emit('BatchSubmitted', batch_submitted, int(time.time()))

    def onBatchStarted(self, batch_submitted: Any) -> None:
        self.__emitter.emit('BatchStarted', batch_submitted, int(time.time()))

    def onOutputOperationStarted(self, output_operation_started: Any) -> None:
        self.__emitter.emit('OutputOperationStarted', output_operation_started, int(time.time()))

    def onOutputOperationCompleted(self, output_operation_completed: Any) -> None:
        self.__emitter.emit('OutputOperationCompleted', output_operation_completed, int(time.time()))
