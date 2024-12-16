from fastapi import FastAPI
import json
from model.Model import ResponseModel, EvaluationModel, Operation
from database.Database import get_db
from database.Operations import get_agents, upload_input_data, get_question_data
from agents.AgentArchetype import Agent
from agents.AgentInitialisation import iniatialise_agents
from utilities.PromptTemplates import entity_extraction_message, operation_chains_message
from utilities.OperationExecutor import OperationChainExecutor

app = FastAPI()

# Initialise our database
db = get_db()

# Upload out data from a pre-processed JSON
json_file_path = "data/ConvFincQA_data.json"
upload_input_data(db, json_file_path)

# Go to our database and grab our agents and initialise them
agent_data = get_agents(db)
agent_pod = iniatialise_agents(agent_data)

@app.get("/")
async def root():
    return {"Hello World"}

@app.post("/answer_question", response_model=ResponseModel)
async def answer_question(response_model: ResponseModel):
    """
    Endpoint to get a basic response message.
    """

    question_metadata = get_question_data(db, response_model.message)

    
    operation_chain_message = operation_chains_message(
        response_model.message, 
        question_metadata.pre_text,
        question_metadata.post_text,
        question_metadata.table_ori
        )
    
    operation_steps = agent_pod["program_builder"].get_response(operation_chain_message).choices[0].message.content
    
    operation_steps_json = json.loads(operation_steps)
    
    print(operation_steps)
    
    entity_extractor_message = entity_extraction_message(
        operation_steps_json, 
        question_metadata.pre_text,
        question_metadata.post_text,
        question_metadata.table_ori
        )
    
    
    response_content = agent_pod["entity_extractor"].get_response(entity_extractor_message).choices[0].message.content
    
    extracted_entities_steps_json = json.loads(response_content)
    
    operations = [
        Operation(step=step['step'], operation=step['op'], arg_1=step['arg1'], arg_2=step['arg2'])
        for step in extracted_entities_steps_json['steps']
    ]
    
    try:
        executor = OperationChainExecutor(operations)
        result = executor.execute()
    except:
        result = "Could not execute operation chain"
    
    print(operations)
    print(result)
    
    executor = OperationChainExecutor(operations)
    result = executor.execute()

    
    response = ResponseModel(
        message=str(result),
        status="Success"
    )
    return response

@app.get("/get_evaluation", response_model=EvaluationModel)
async def get_evaluation():
    """
    Endpoint to get an evaluation.
    """
    evaluation = {
        "score": 85,
        "feedback": "Good job! Keep it up!"
    }
    return evaluation

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    