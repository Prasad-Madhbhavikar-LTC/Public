import json
import logging
import time

from emitters import AbstractEmitter

LOGGER = logging.getLogger(__name__)


class LoggingEmitter(AbstractEmitter):
    def __init__(self, producer: AbstractEmitter):
        super().__init__("LoggingProducer")
        self.__producer = producer
        LOGGER.info(f"Initialized LoggingProducer Producer for {self.__producer._producer_name}")

    def emit(self, event_name: str, event_data: object, event_creation_time: int) -> None:
        message = {
            "meta": {
                "source": self._producer_name,
                "creation_time": event_creation_time * 1000,
                "received_time": int(time.time() * 1000)
            },
            "data": {
                "event_name": event_name,
                "event_data": AbstractEmitter._convert_java_object(event_data)
            }
        }

        LOGGER.info(
            f"Sent event {event_name} to LoggingProducer  {self.__producer._producer_name}: {json.dumps(message).encode('utf-8')}")
