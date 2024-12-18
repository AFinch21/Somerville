from nicegui import ui
import requests
from APICalls import get_questions, get_response
from FrontendFucntions import match_arguments, convert_operations, convert_arguments
import json

question_dta = get_questions()

operation_values = []  # Declare the operations list at the top level
operation_values_true = []
operation_arguments = []
contexts = {
    'pre_text' : [],
    'table_ori' : [],
    'post_text' : []
}
matched_arguments = []
llm_answer = 0.0
exe_answer = 0.0

# Counter function
@ui.refreshable
def dynamic_step_display():
    with ui.row().classes('justify-between items-center'):
        for index, operation in enumerate(operation_arguments):
            with ui.card().classes('w-60'):
                with ui.column().classes('w-full items-center'):
                    with ui.row():
                        ui.label("Step:").style('color: #000000; font-size: 100%; font-weight: 300')
                        ui.label(operation['step']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                    with ui.row():
                        ui.label("Operation:").style('color: #000000; font-size: 100%; font-weight: 300')
                        ui.label(operation['operation']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                with ui.column().classes('w-full items-center'):
                    with ui.row():
                        ui.label("Arg 1:").style('color: #000000; font-size: 100%; font-weight: 300')
                        ui.label(operation['arg_1']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                    with ui.row():
                        ui.label("Arg 2:").style('color: #000000; font-size: 100%; font-weight: 300')
                        ui.label(operation['arg_2']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                # ui.label(f'Count = {count}').classes(f'text-{color}')
            if len(operation_arguments) > 1 and index != (len(operation_arguments)-1):
                ui.icon('chevron_right', size='50px')

@ui.refreshable   
def dynamic_calculation_display():
    with ui.row().classes('justify-between items-center'):
        for index, operation in enumerate(operation_values):
            with ui.card().classes('w-60'):
                with ui.column().classes('w-full items-center'):
                    with ui.row():
                        ui.label("Step:").style('color: #000000; font-size: 100%; font-weight: 300')
                        ui.label(operation['step']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                    with ui.row():
                        ui.label("Operation:").style('color: #000000; font-size: 100%; font-weight: 300')
                        ui.label(operation['operation']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                with ui.column().classes('w-full items-center'):
                    with ui.row():
                        ui.label("Arg 1:").style('color: #000000; font-size: 100%; font-weight: 300')
                        ui.label(operation['arg_1']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                    with ui.row():
                        ui.label("Arg 2:").style('color: #000000; font-size: 100%; font-weight: 300')
                        ui.label(operation['arg_2']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                # ui.label(f'Count = {count}').classes(f'text-{color}')
            if len(operation_values) > 1 and index != (len(operation_values)-1):
                ui.icon('chevron_right', size='50px')
        ui.icon('chevron_right', size='50px')
        with ui.card().classes('w-60'):
            with ui.column().classes('w-full items-center'):
                with ui.row():
                    ui.label("Answer:").style('color: #000000; font-size: 100%; font-weight: 300')
                    ui.label(llm_answer).style('color: #6E93D6; font-size: 100%; font-weight: 300')

# Counter function
@ui.refreshable
def dynamic_comparison_display():
            
            with ui.grid(columns=2).classes("w-full"):  # Display one card per row
                with ui.column():
                    answer_text_colour = 'green' if (round(float(llm_answer), 3)) == round(float(exe_answer), 3) else 'red'
                    answer_steps_colour = 'green' if (len(operation_values_true)) == round(len(operation_values)) else 'red'
                    
                    ui.label('Predicted Answer (as float)').classes('text-lg mb-4 text-blue-600 font-bold')
                    ui.label(round(float(llm_answer), 3)).classes(f'text-lg mb-4 text-{answer_text_colour}-600 font-bold')
                    ui.label('Predicted steps #').classes('text-lg mb-4 text-blue-600 font-bold')
                    ui.label(len(operation_values)).classes(f'text-lg mb-4 text-{answer_steps_colour}-600 font-bold')
                    ui.label('Predicted Steps').classes('text-lg mb-4 text-blue-600 font-bold')
                    for index, operation in enumerate(operation_values):
                        
                        # Determine card color based on correctness (to be added below)
                        left_color = 'bg-green-100' if (
                            operation.get("step") == (index+1) and
                            operation.get("operation") == convert_operations(operation_values_true[index].get("op")) and
                            operation.get("arg_1") == convert_arguments(operation_values_true[index].get("arg1")) and
                            operation.get("arg_2") == convert_arguments(operation_values_true[index].get("arg2"))
                        ) else 'bg-red-100'
                        
                        with ui.card().classes(f'w-60 {left_color} shadow-lg'):  # Add shadow for styling
                            with ui.row():
                                ui.label(f"Step: {operation.get('step')}").style('font-size: 14px; font-weight: bold')
                            with ui.row():
                                ui.label(f"Operation: {operation.get('operation')}").style('color: #6E93D6; font-weight: 400')
                            with ui.row():
                                ui.label(f"Arg 1: {operation.get('arg_1')}").style('color: #333; font-weight: 400')
                            with ui.row():
                                ui.label(f"Arg 2: {operation.get('arg_2')}").style('color: #333; font-weight: 400')

                with ui.column():  # Display one card per row
                    ui.label('ConvFinQA Answer (as float)').classes('text-lg mb-4 text-green-600 font-bold')
                    ui.label(round(float(exe_answer), 3)).classes('text-lg mb-4 text-black-600 font-bold')
                    ui.label('ConvFinQA suggested steps #').classes('text-lg mb-4 text-green-600 font-bold')
                    ui.label(len(operation_values_true)).classes('text-lg mb-4 text-black-600 font-bold')
                    ui.label('ConvFinQA Steps').classes('text-lg mb-4 text-green-600 font-bold')
                    for index, operation in enumerate(operation_values_true):
                        # No color coding for the true operations, as they're assumed correct
                        with ui.card().classes('w-60 bg-white shadow-lg'):
                            with ui.row():
                                ui.label(f"Step: {(index+1)}").style('font-size: 14px; font-weight: bold')
                            with ui.row():
                                ui.label(f"Operation: {convert_operations(operation.get('op'))}").style('color: #6E93D6; font-weight: 400')
                            with ui.row():
                                ui.label(f"Arg 1: {convert_arguments(operation.get('arg1'))}").style('color: #333; font-weight: 400')
                            with ui.row():
                                ui.label(f"Arg 2: {convert_arguments(operation.get('arg2'))}").style('color: #333; font-weight: 400')

@ui.refreshable
def dynamic_context_display():
    with ui.splitter() as splitter:
        with splitter.before:
            with ui.column().classes('w-full items-center'):
                with ui.row():
                    ui.label("Pre-Text:").style('color: #000000; font-size: 125%; font-weight: 300')
                with ui.row():
                    ui.label(contexts['pre_text']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                with ui.row():    
                    ui.label("Table:").style('color: #000000; font-size: 125%; font-weight: 300')
                with ui.row():
                    ui.label(contexts['table_ori']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                with ui.row():  
                    ui.label("Post-Text:").style('color: #000000; font-size: 125%; font-weight: 300')
                with ui.row():
                    ui.label(contexts['post_text']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
        with splitter.after:
            for argument in matched_arguments:
                with ui.column().classes('w-full items-center'):
                    ui.space()
                    with ui.card().classes('w-60'):
                        with ui.row():
                            ui.label("Step:").style('color: #000000; font-size: 100%; font-weight: 300')
                            ui.label(argument['step']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                        with ui.row():
                            ui.label("Extracted Argument 1:").style('color: #000000; font-size: 100%; font-weight: 300')
                            ui.label(argument['arg_1']['description']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                        with ui.row():
                            ui.label("Value:").style('color: #000000; font-size: 100%; font-weight: 300')
                            ui.label(argument['arg_1']['value']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                        with ui.row():
                            ui.label("Extracted Argument 2:").style('color: #000000; font-size: 100%; font-weight: 300')
                            ui.label(argument['arg_2']['description']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                        with ui.row():
                            ui.label("Value:").style('color: #000000; font-size: 100%; font-weight: 300')
                            ui.label(argument['arg_2']['value']).style('color: #6E93D6; font-size: 100%; font-weight: 300')
                    ui.space()



async def on_go_button_click(question):
    global operation_arguments  # Explicitly declare that we're modifying the global operations list
    global operation_values
    global operation_values_true
    global contexts
    global matched_arguments
    global llm_answer
    global exe_answer
    
    question = question.value  # Get the value from the input field
    
    print(question)
    
    
    pre_text = [record['pre_text'] for record in question_dta if record.get('question') == question]
    table = [record['table_ori'] for record in question_dta if record.get('question') == question]
    post_text = [record['post_text'] for record in question_dta if record.get('question') == question]
    exe_answer = next((record['exe_answer'] for record in question_dta if record.get('question') == question), None)
    operation_values_true = [record['steps'] for record in question_dta if record.get('question') == question][0]
    operation_steps_true = operation_values_true.replace("'", '"')
    operation_values_true = json.loads(operation_steps_true)
    contexts = {
        'pre_text' : pre_text,
        'table_ori' : table,
        'post_text' : post_text
    }

    response = await get_response(question)  # Process the input value
    print(operation_values_true)
    # temp_ops = [{'step': 1, 'operation': 'Add', 'arg_1': 0.0, 'arg_2': 0.0}, {'step': 2, 'operation': 'Add', 'arg_1': 0.0, 'arg_2': 0.0}, {'step': 3, 'operation': 'Add', 'arg_1': 0.0, 'arg_2': 0.0}]
    operation_values = response['operations']  # Update the global operations list dynamically
    operation_arguments = response['operation_arguments']
    matched_arguments = match_arguments(operation_arguments, operation_values)
    llm_answer = response['answer']

    dynamic_step_display.refresh()
    dynamic_context_display.refresh()
    dynamic_calculation_display.refresh()
    dynamic_comparison_display.refresh()

@ui.page('/')
def index():
    # Banner with navigation buttons
    with ui.header().classes('justify-between items-center'):
        with ui.row():
            ui.markdown("### Somerville.ai")
        with ui.row():
            ui.button("Home", on_click=lambda: print("Home clicked"))
            ui.button("Evaluation", on_click=lambda: print("Evaluation clicked"))
            ui.button("About", on_click=lambda: print("About clicked"))

    with ui.column().classes('w-full items-center'):
        with ui.row():
            label = "Welcome to Somerville - an LLM-powered financial arithmetic solution. "
            ui.label(label).style('font-size: 22px; color: #008B8B')
            
        def update_questions():
            question.clear()  # Clear the current options in the question dropdown
            filtered_questions = [record['question'] for record in question_dta if record.get('company') == company.value]
            question.set_options(filtered_questions, value=filtered_questions[0])  # Add the updated options to the question dropdown

        with ui.row().style('align-items: center;'):
            company = ui.select(
                options=[x['company'] for x in question_dta],
                value='AAPL',
                label='Company',
                on_change= update_questions,
            ).classes('w-80')

            question = ui.select(
                options=[record['question'] for record in question_dta if record.get('company') == company.value],
                label='Question',
            ).classes('w-80')

        with ui.row().style('align-items: center'):

                

            ui.button("Go!", on_click=lambda: on_go_button_click(question=question)).classes('mt-6')

        with ui.column().classes('w-full items-center'):
            with ui.row().classes('w-2/3'):
                with ui.tabs().classes("w-full") as tabs:
                    plan = ui.tab('Plan', icon='turn_sharp_right').classes("text-cyan w-full")
                    extract = ui.tab('Extract', icon='checklist_rtl').classes("text-cyan w-full")
                    calculate = ui.tab('Calculate', icon='calculate').classes("text-cyan w-full")
                    evaluate = ui.tab('Evaluate', icon='add_task').classes("text-cyan w-full")
                
                with ui.tab_panels(tabs, value=plan).classes('w-full'):
                    with ui.tab_panel(plan):
                        ui.label('First Tab - Dynamic Counters')
                        dynamic_step_display()  # Display counters dynamically

                    with ui.tab_panel(extract):
                        ui.label('Second tab')
                        dynamic_context_display()

                    with ui.tab_panel(calculate):
                        ui.label('Third tab')
                        dynamic_calculation_display()

                    with ui.tab_panel(evaluate):
                        ui.label('Fourth tab')
                        dynamic_comparison_display()
        
    with ui.row().style('align-items: center'):
        
        ui.space()
        result = ui.label("")
        


        


ui.run()
