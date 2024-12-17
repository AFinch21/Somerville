from APICalls import get_response

def match_arguments(steps_with_descriptions, extracted_steps):
    # Create a new object to store the matched result
    new_object = []
    
    # Iterate through both the descriptive and extracted steps
    for description_step, extracted_step in zip(steps_with_descriptions, extracted_steps):
        # Create a dictionary for the current step
        step_data = {'step': description_step['step']}
        
        # Add arguments with descriptions and values
        for arg_key in ['arg_1', 'arg_2']:
            step_data[arg_key] = {
                'description': description_step[arg_key],  # Argument description
                'value': extracted_step[arg_key]  # Corresponding extracted value
            }
        
        # Append the processed step data
        new_object.append(step_data)
    
    return new_object