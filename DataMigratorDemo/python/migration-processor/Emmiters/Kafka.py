import json
import logging
import time
from confluent_kafka import Producer

from Emmiters import AbstractEmitter

logger = logging.getLogger(__name__)


class KafkaEmitter(AbstractEmitter):
    def __init__(self, kafka_config: object, topic_name: str):
        super().__init__("Kafka")
        self.__kafka_producer = Producer(kafka_config)
        self.__topic_name = topic_name
        logger.info(f"Initialized Kafka Producer for {topic_name}")

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

        self.__kafka_producer.produce(self.__topic_name, key=event_name, value=json.dumps(message).encode('utf-8'))
        logger.debug(f"Sent event {event_name} to Kafka: {message}")
        self.__kafka_producer.flush()
