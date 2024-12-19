import unittest
from model.Model import Operation
from utilities.OperationExecutor import OperationChainExecutor  # Update with the correct module name

class TestOperationChainExecutor(unittest.TestCase):

    def setUp(self):
        # Common operations for testing
        self.operations = [
            Operation(step=1, operation='Add', arg_1=5, arg_2=3),
            Operation(step=2, operation='Multiply', arg_1="step_1", arg_2=2),
            Operation(step=3, operation='Subtract', arg_1="step_2", arg_2=4),
            Operation(step=4, operation='Divide', arg_1="step_3", arg_2=2)
        ]

    def test_execute(self):
        executor = OperationChainExecutor(self.operations)
        result = executor.execute()
        self.assertAlmostEqual(result, 6.0)

    def test_invalid_operation(self):
        # Include an unsupported operation
        operations = [
            Operation(step=1, operation='Add', arg_1=5, arg_2=3),
            Operation(step=2, operation='Power', arg_1="step_1", arg_2=2)  # Unsupported
        ]
        executor = OperationChainExecutor(operations)
        with self.assertRaises(ValueError):
            executor.execute()

    def test_multiple_steps(self):
        executor = OperationChainExecutor(self.operations)
        executor.execute()
        # Validate intermediate results
        self.assertEqual(executor.results["step_1"], 8)
        self.assertEqual(executor.results["step_2"], 16)
        self.assertEqual(executor.results["step_3"], 12)
        self.assertAlmostEqual(executor.results["step_4"], 6.0)

    def test_division_by_zero(self):
        operations = [
            Operation(step=1, operation='Add', arg_1=5, arg_2=3),
            Operation(step=2, operation='Divide', arg_1="step_1", arg_2=0)
        ]
        executor = OperationChainExecutor(operations)
        with self.assertRaises(ZeroDivisionError):
            executor.execute()

    def test_float_operations(self):
        operations = [
            Operation(step=1, operation='Add', arg_1=1.5, arg_2=2.5),
            Operation(step=2, operation='Multiply', arg_1="step_1", arg_2=2)
        ]
        executor = OperationChainExecutor(operations)
        result = executor.execute()
        self.assertAlmostEqual(result, 8.0)