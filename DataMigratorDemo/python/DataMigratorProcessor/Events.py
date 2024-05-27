from abc import ABC, abstractmethod

class EventProducer(ABC):
    def __init__(self, producer_name) -> None:
        self._producer_name = producer_name

    @abstractmethod
    def send_event(self, event_name, event_data, event_creation_time : int):
        raise NotImplementedError("Subclass must implement send_event() method")