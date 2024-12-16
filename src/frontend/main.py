from nicegui import ui
import requests
from APICalls import get_questions, get_response

question_dta = get_questions()

print(question_dta[0:10])

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
            label = "Welcome to Somerville - an LLM-powered financial arithmatic solution."
            ui.label(label).style('font-size: 22px; color: #008B8B')
            
        with ui.column():
            with ui.row():
                with ui.tabs().classes('w-full') as tabs:
                    plan = ui.tab('Plan', icon='turn_sharp_right').classes("text-cyan")
                    extract = ui.tab('Extract', icon='checklist_rtl').classes("text-cyan")
                    calculate = ui.tab('Calculate', icon='calculate').classes("text-cyan")
                    evaluate = ui.tab('Evaluate', icon='add_task').classes("text-cyan")
                with ui.tab_panels(tabs, value=plan).classes('w-full'):
                    with ui.tab_panel(plan):
                        ui.label('First tab')
                    with ui.tab_panel(extract):
                        ui.label('Second tab')
                    with ui.tab_panel(calculate):
                        ui.label('Third tab')
                    with ui.tab_panel(evaluate):
                        ui.label('Fourth tab')
        

        with ui.row().style('align-items: center;'):
            with ui.row().style('align-items: center'):
                company = ui.select([x['company'] for x in question_dta], value= 'AAPL',label='Company', on_change=lambda: print(company.value))
                # year = ui.select([record['year'] for record in question_dta if record.get('company') == company.value], label='Year',on_change=lambda: print(year.value))
                question = ui.select([record['question'] for record in question_dta if record.get('company') == company.value], label='Question')

        with ui.row().style('align-items: center'):
            def on_go_button_click():
                value = question.value  # Get the value from the input field
                response = get_response(value)  # Process the input value
                result.text = f'{response['answer']}'  # Update the label dynamically

            ui.button("Go!", on_click=on_go_button_click).classes('mt-6')
            
            
        with ui.row().style('align-items: center'):
            
            ui.space()
            result = ui.label("")

        


ui.run()