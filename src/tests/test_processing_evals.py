import unittest
from model.Model import EvaluationSummary, EvaluationResponse, Operation
from utilities.ProcessEvalResults import process_evaluation_run, calculate_correct_answer_percentage, calculate_step_accuracy_percentage

class MockObject:
    """Mock object to simulate input."""
    def __init__(self, answer, true_answer, predicted_steps, true_steps):
        self.answer = answer
        self.true_answer = true_answer
        self.predicted_steps = predicted_steps
        self.true_steps = true_steps

class TestEvaluationRun(unittest.TestCase):
    def test_correct_answer_percentage(self):
        results = [
            MockObject(answer=5, true_answer=5, predicted_steps=3, true_steps=3),
            MockObject(answer=4.123, true_answer=4.124, predicted_steps=2, true_steps=3),
            MockObject(answer=3.333, true_answer=3.333, predicted_steps=4, true_steps=4),
        ]
        percentage, num_correct = calculate_correct_answer_percentage(results)
        self.assertEqual(percentage, (2 / 3) * 100)
        self.assertEqual(num_correct, 2)

    def test_step_accuracy_percentage(self):
        results = [
            MockObject(answer=5, true_answer=5, predicted_steps=3, true_steps=3),
            MockObject(answer=4.123, true_answer=4.124, predicted_steps=2, true_steps=3),
            MockObject(answer=3.333, true_answer=3.333, predicted_steps=4, true_steps=4),
        ]
        step_accuracy = calculate_step_accuracy_percentage(results)
        self.assertEqual(step_accuracy, (2 / 3) * 100)

class TestEvaluationRunWithEvaluationResponse(unittest.TestCase):
    def test_process_evaluation_run(self):
        
        operations = [
            Operation(
                step=1,
                operation="Subtract",
                arg_1=1.5,
                arg_2=2.5
            ),
            Operation(
                step=2,
                operation="Subtract",
                arg_1=1.5,
                arg_2=2.5
            ),
            Operation(
                step=3,
                operation="Subtract",
                arg_1=1.5,
                arg_2=2.5
            )
        ]
        
        
        results = [
            EvaluationResponse(
                question="What is 2 + 3?", 
                answer=5, 
                predicted_operations=operations, 
                predicted_steps=1, 
                input_tokens=5, 
                ouput_tokens=2, 
                latency=50.0, 
                true_steps=1, 
                true_program="add(2, 3)", 
                true_answer=5
            ),
            EvaluationResponse(
                question="What is 2.123 + 2?", 
                answer=4.123, 
                predicted_operations=operations, 
                predicted_steps=2, 
                input_tokens=10, 
                ouput_tokens=4, 
                latency=100.0, 
                true_steps=3, 
                true_program="add(2.123, 2)", 
                true_answer=4.124
            ),
            EvaluationResponse(
                question="What is 3.333 rounded to 3 decimals?", 
                answer=3.333, 
                predicted_operations=operations, 
                predicted_steps=1, 
                input_tokens=12, 
                ouput_tokens=6, 
                latency=150.0, 
                true_steps=1, 
                true_program="[{'op': 'multiply2-1', 'arg1': '11.6', 'arg2': 'const_1000', 'res': '11600'}, {'op': 'divide2-2', 'arg1': '#0', 'arg2': '13280', 'res': '87%'}]", 
                true_answer=3.333
            ),
        ]

        summary = process_evaluation_run(results)

        # Assertions for the EvaluationSummary
        self.assertIsInstance(summary, EvaluationSummary)
        self.assertEqual(summary.num_eval_questions, len(results))
        self.assertEqual(summary.num_answered_questions, len(results))
        self.assertEqual(summary.num_correct_answers, 2)  # Questions 1 and 3 are correct.
        self.assertEqual(summary.answer_accuracy, (2 / 3) * 100)
        self.assertEqual(summary.step_accuracy, (2 / 3) * 100)
        self.assertEqual(summary.average_latency, 100.0)
        self.assertEqual(summary.max_latency, 100.0)
        self.assertEqual(summary.min_latency, 100.0)