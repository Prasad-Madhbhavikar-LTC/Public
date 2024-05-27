from abc import ABC, abstractmethod
from QualityChecks import QualityChecks

class AbstractInterpreter(ABC):
     
    @abstractmethod
    def parse(self, feature):
        raise NotImplementedError("Subclass must implement interpret() method")
    
    @abstractmethod
    def interpret(self, parsed_features) -> QualityChecks:
        raise NotImplementedError("Subclass must implement interpret() method")
    
    @abstractmethod
    def run(self, check : QualityChecks, data):
        raise NotImplementedError("Subclass must implement run() method")
    
