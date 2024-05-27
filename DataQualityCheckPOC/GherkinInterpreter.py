from abc import abstractmethod
from Interpreter import AbstractInterpreter
from gherkin.parser import Parser
from gherkin.errors import CompositeParserException

from QualityChecks import QualityChecks

class AbstractGherkinInterpreter(AbstractInterpreter):
    def parse(self, feature):
            return_value = None
            errors = []

            try:
                with open(feature, 'r') as file:
                    parser = Parser()
                    return_value = parser.parse(file.read())
                print("Syntax is valid")
            except CompositeParserException as e:
                return_value = False
                for error in e.errors:
                    errors.append({
                        "line": error.location['line'],
                        "column" : error.location['column'],
                        "message": error.args
                    }) 
            return return_value, errors
    
    @abstractmethod
    def interpret(self, parsed_features) -> QualityChecks:
        raise NotImplementedError("Subclass must implement interpret() method")
    
    @abstractmethod
    def run(self, check : QualityChecks, data):
        raise NotImplementedError("Subclass must implement run() method")