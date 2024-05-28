from GherkinInterpreter import GherkinInterpreter
from pydeequ.checks import *
from pydeequ.verification import *
from pyspark.sql import SparkSession

from QualityChecks import QualityChecks

class PyDeeQuInterpreter(GherkinInterpreter):

    def __init__(self, spark_session: SparkSession) -> None:
        self.__spark_session = spark_session
        super().__init__()

    def interpret(self, ast) -> QualityChecks:
       
        check = Check(self.__spark_session, CheckLevel.Warning, "Data Quality Check")
        
        for scenario in ast['scenarioDefinitions']:
            for step in scenario['steps']:
                field = step['text'].split(' ')[-1]  # Get the field name from the step text
                if 'not null' in step['text']:
                    check = check.isNotNull(field)
                elif 'not be an empty string' in step['text']:
                    check = check.isNonEmpty(field)
                elif 'should be valid' in step['text']:
                    check = check.isComplete(field)  # Assuming 'valid' means 'not null'
                elif 'associated with only one' in step['text']:
                    check = check.isUnique(field)
                elif 'should be positive' in step['text']:
                    check = check.isPositive(field)
                elif 'should be negative' in step['text']:
                    check = check.isNegative(field)
                elif 'should be in range' in step['text']:
                    # Assuming the range is specified as (min, max) in the step text
                    min_val, max_val = map(int, step['text'].split(' ')[-1].strip('()').split(','))
                    check = check.isContainedInRange(field, min_val, max_val)
                elif 'should be one of' in step['text']:
                    # Assuming the allowed values are specified as a list in the step text
                    allowed_values = step['text'].split(' ')[-1].strip('[]').split(',')
                    check = check.isInAllowedValues(field, allowed_values)
                elif 'should be less than' in step['text']:
                    # Assuming the threshold is specified in the step text
                    threshold = float(step['text'].split(' ')[-1])
                    check = check.isLessThan(field, threshold)
                elif 'should be greater than' in step['text']:
                    # Assuming the threshold is specified in the step text
                    threshold = float(step['text'].split(' ')[-1])
                    check = check.isGreaterThan(field, threshold)
                elif 'should be less than or equal to' in step['text']:
                    # Assuming the threshold is specified in the step text
                    threshold = float(step['text'].split(' ')[-1])
                    check = check.isLessThanOrEqualTo(field, threshold)
                elif 'should be greater than or equal to' in step['text']:
                    # Assuming the threshold is specified in the step text
                    threshold = float(step['text'].split(' ')[-1])
                    check = check.isGreaterThanOrEqualTo(field, threshold)
                elif 'should be equal to' in step['text']:
                    # Assuming the value is specified in the step text
                    value = step['text'].split(' ')[-1]
                    check = check.isEqualTo(field, value)
                elif 'should not be equal to' in step['text']:
                    # Assuming the value is specified in the step text
                    value = step['text'].split(' ')[-1]
                    check = check.isNotEqualTo(field, value)
                elif 'should satisfy' in step['text']:
                    # Assuming the condition is specified as a Python lambda function in the step text
                    condition = eval(step['text'].split(' ')[-1])
                    check = check.satisfies(field, condition)
    
        return QualityChecks(check)

    def run(self, check : QualityChecks, data):
        verification_result = VerificationSuite(self.__spark_session).onData(data).addCheck(check.get_checks()).run()
        return verification_result.toJSON()