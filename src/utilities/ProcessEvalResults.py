
from model.Model import EvaluationSummary

def process_evaluation_run(results: list) -> EvaluationSummary:
    
    correct_answer_percentage, correct_answers = calculate_correct_answer_percentage(results)
    
    correct_step_percentage = calculate_step_accuracy_percentage(results)
    
    return EvaluationSummary(
        responses=results,
        num_eval_questions=len(results),
        num_answered_questions=len(results),
        num_correct_answers=correct_answers,
        answer_accuracy=correct_answer_percentage,
        step_accuracy=correct_step_percentage,
        average_latency=100.0,
        max_latency=100.0,
        min_latency=100.0
    )
    
def calculate_correct_answer_percentage(objects):
    total_answers = len(objects)  # Total number of answers
    correct_answers = 0  # Counter for correct answers

    for obj in objects:
        # Compare each object's 'answer' with 'true_answer'
        # If they're equal (or, optionally, within a small margin for floating-point precision), it's correct
        try:
            if round(obj.answer, 3) == round(obj.true_answer, 3):
                correct_answers += 1
        except:
            continue

    # Calculate the percentage of correct answers
    correct_percentage = (correct_answers / total_answers) * 100
    
    return correct_percentage, correct_answers

def calculate_step_accuracy_percentage(objects):
    total_answers = len(objects)  # Total number of answers
    correct_steps_count = 0  # Counter for answers with correct step count

    for obj in objects:
        # Compare each object's 'predicted_steps' with 'true_steps'
        if obj.predicted_steps == obj.true_steps:
            correct_steps_count += 1

    # Calculate the percentage of answers with correct step count
    step_accuracy_percentage = (float(correct_steps_count) / float(total_answers)) * 100
    
    return step_accuracy_percentage