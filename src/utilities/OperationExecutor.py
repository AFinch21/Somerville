from typing import List
from dataclasses import dataclass
from model.Model import Operation

class OperationChainExecutor:
    def __init__(self, operations: List[Operation]):
        # Sort operations by step
        self.operations = sorted(operations, key=lambda x: x.step)
        self.results = {}

    def execute_operation(self, operation: Operation):
        op_type = operation.operation
        arg_1 = operation.arg_1
        arg_2 = operation.arg_2

        # Resolve arguments
        value1 = self.results.get(arg_1, arg_1)
        value2 = self.results.get(arg_2, arg_2)

        # Ensure arguments are numbers; first convert to string for checking if it contains a decimal
        value1 = float(value1) if '.' in str(value1) else int(value1)
        value2 = float(value2) if '.' in str(value2) else int(value2)

        # Perform the operation
        if op_type == 'Subtract':
            result = value1 - value2
        elif op_type == 'Divide':
            result = value1 / value2
        elif op_type == 'Add':
            result = value1 + value2
        elif op_type == 'Multiply':
            result = value1 * value2
        else:
            raise ValueError(f"Unsupported operation: {op_type}")

        # Store the result for later operations
        self.results[f"step_{operation.step}"] = result

    def execute(self):
        for operation in self.operations:
            self.execute_operation(operation)
        # Return the result of the last operation
        return self.results[f"step_{self.operations[-1].step}"]
    
