from APICalls import get_response
import string

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

def convert_operations(operation):
    if 'minus' in operation:
        return 'Subtract'
    if 'divide' in operation:
        return 'Divide'
    if 'add' in operation:
        return 'Add'
    if 'multiply' in operation:
        return 'Multiply'
    else:
        return operation
    
def convert_arguments(argument):
    # Check if the argument is a string and starts with "#"
    if isinstance(argument, str) and argument.startswith("#"):
        # Extract the numeric value after "#" and convert it for step comparison
        try:
            step_num = int(argument[1:]) + 1  # e.g., "#0" -> 0 -> "step_1"
            return f"step_{step_num}"
        except ValueError:
            raise ValueError(f"Invalid argument format: {argument}, expected something like '#0'")
    
    # Check if the argument is a string and starts with "const_"
    if isinstance(argument, str) and argument.startswith("const_"):
        # Extract the numeric value after "const_" and return it
        parts = argument.split("_")
        if len(parts) > 1:  # Ensure there's a numeric part after the underscore
            try:
                return float(parts[1])  # Extract the numeric portion
            except ValueError:
                raise ValueError(f"Invalid argument format: {argument}, expected something like 'const_100'")
        else:
            raise ValueError(f"Invalid argument format: {argument}, expected something like 'const_100'")
    
    # Check if the argument is a numeric string and try converting it to float
    try:
        return float(argument)  # e.g., "338" -> 338.0
    except (ValueError, TypeError):
        raise ValueError(f"Cannot convert argument to float: {argument}")
    
def comparison_debugger(index, operation, operation_values_true):
    print(f"\n--- Debugging Step {index+1} ---")
    print(f"Step in operation: {operation.get('step')} vs Step in index: {index + 1}")
    print(f"Operation in 'operation': {operation.get('operation')}")
    print(f"Operation in 'operation_values_true': {operation_values_true[index].get('op')}")
    print(f"Converted Operation: {convert_operations(operation_values_true[index].get('op'))}")
    print(f"Arg 1 in 'operation': {operation.get('arg_1')}")
    print(f"Arg 1 in 'operation_values_true': {operation_values_true[index].get('arg1')}")
    print(f"Converted Arg 1: {convert_argmuents(operation_values_true[index].get('arg1'))}")
    print(f"Arg 2 in 'operation': {operation.get('arg_2')}")
    print(f"Arg 2 in 'operation_values_true': {operation_values_true[index].get('arg2')}")
    print(f"Converted Arg 2: {convert_argmuents(operation_values_true[index].get('arg2'))}")
