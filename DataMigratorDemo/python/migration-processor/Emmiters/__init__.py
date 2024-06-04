__all__ = [
    "Kafka",
    "Logging"
]

import logging
from abc import ABC, abstractmethod

LOGGER = logging.getLogger(__name__)


class AbstractEmitter(ABC):
    def __init__(self, producer_name: str) -> None:
        super().__init__()
        self._producer_name = producer_name

    @abstractmethod
    def emit(self, event_name: str, event_data: object, event_creation_time: int) -> None:
        raise NotImplementedError("Subclass must implement send_event() method")

    @staticmethod
    def _convert_java_object(obj: object) -> object:
        if AbstractEmitter._is_java_object(obj):
            LOGGER.debug("Object is of type JAVA")
            python_dict = {}
            for field in obj.getClass().getDeclaredFields():
                field.setAccessible(True)
                name = field.getName()
                value = field.get(obj)
                if isinstance(value, (str, int, float)):
                    python_dict[name] = AbstractEmitter._convert_java_object(value)
                else:
                    LOGGER.debug("Object type is not str, int, float, would be ignored")
            return python_dict
        elif isinstance(obj, dict):
            LOGGER.debug("Object is of type dict")
            new_dict = {}
            for key, value in obj.items():
                if isinstance(value, (str, int, float)):
                    new_dict[key] = AbstractEmitter._convert_java_object(value)
                else:
                    LOGGER.debug("Object type is not str, int, float, would be ignored")
            return new_dict
        else:
            LOGGER.debug("Simple object detected")
            return obj

    @staticmethod
    def _is_java_object(obj: object) -> bool:
        return 'JavaObject' in str(type(obj))
