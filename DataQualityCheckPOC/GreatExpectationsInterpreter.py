from GherkinInterpreter import GherkinInterpreter
import great_expectations as ge

from QualityChecks import QualityChecks

class GreatExpectationsInterpreter(GherkinInterpreter):

    def __init__(self) -> None:
        super().__init__()

    def interpret(self, ast, data):
        df = ge.dataset.SparkDFDataset(data)
        
        for scenario in ast['scenarioDefinitions']:
            for step in scenario['steps']:
                field = step['text'].split(' ')[-1]  # Get the field name from the step text
                if 'not null' in step['text']:
                    df.expect_column_values_to_not_be_null(field)
                elif 'not be an empty string' in step['text']:
                    df.expect_column_values_to_not_be_in_set(field, [""])
                elif 'should be valid' in step['text']:
                    df.expect_column_values_to_not_be_null(field)  # Assuming 'valid' means 'not null'
                elif 'associated with only one' in step['text']:
                    df.expect_column_pair_values_A_to_be_unique_within_record(field, 'email')
                elif 'should be positive' in step['text']:
                    df.expect_column_values_to_be_between(field, min_value=0)
                elif 'should be negative' in step['text']:
                    df.expect_column_values_to_be_between(field, max_value=0)
                elif 'should be in range' in step['text']:
                    # Assuming the range is specified as (min, max) in the step text
                    min_val, max_val = map(int, step['text'].split(' ')[-1].strip('()').split(','))
                    df.expect_column_values_to_be_between(field, min_value=min_val, max_value=max_val)
                elif 'should be one of' in step['text']:
                    # Assuming the allowed values are specified as a list in the step text
                    allowed_values = step['text'].split(' ')[-1].strip('[]').split(',')
                    df.expect_column_values_to_be_in_set(field, allowed_values)
        
        return df.get_expectation_suite()
    

    def run(self, check : QualityChecks, data):
        verification_result = check.get_checks().validate()
        return verification_result
