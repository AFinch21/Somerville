from fastapi import FastAPI
import json
from model.Model import QueryRequest, EvaluationModel, Operation, QueryResponse
from database.Database import get_db
from database.Operations import get_agents, upload_input_data, get_question_data
from agents.AgentArchetype import Agent
from agents.AgentInitialisation import iniatialise_agents
from utilities.PromptTemplates import entity_extraction_message, operation_chains_message
from utilities.OperationExecutor import OperationChainExecutor
from logger.Logger import get_logger

app = FastAPI()

# Get logger
logger = get_logger()

# Initialise our database
db = get_db()

try:
    # Upload out data from a pre-processed JSON
    json_file_path = "data/ConvFincQA_data.json"
    upload_input_data(db, json_file_path)
    logger.info("Data Upload Complete")
except:
    logger.warning("Data Upload failed - please check datafile")

# Go to our database and grab our agents and initialise them
try:
    agent_data = get_agents(db)
    agent_pod = iniatialise_agents(agent_data)
    logger.info("Application set up complete")
except:
    logger.warning("Agent load failed - please check agent database")
    
logger.info("Application setup complete")

@app.get("/")
async def root():
    return {"Hello World"}

@app.post("/answer_question", response_model=QueryResponse)
async def answer_question(query_request: QueryRequest):
    """
    Endpoint to get a basic response message.
    """
    logger.info("Question answer worklfow started")
    logger.info(f"Question: {query_request.message}")
    question_metadata = get_question_data(db, query_request.message)
    
    operation_chain_message = operation_chains_message(
        query_request.message, 
        question_metadata.pre_text,
        question_metadata.post_text,
        question_metadata.table_ori
        )
    
    logger.llm(f'Sending request to {agent_pod['program_builder'].agent_name}...')
    operation_steps = agent_pod["program_builder"].get_response(operation_chain_message).choices[0].message.content
    logger.llm(f'Sending request to {agent_pod['program_builder'].agent_name} executed')
    
    operation_steps_json = json.loads(operation_steps)
    
    entity_extractor_message = entity_extraction_message(
        operation_steps_json, 
        question_metadata.pre_text,
        question_metadata.post_text,
        question_metadata.table_ori
        )
    
    logger.llm(f'Sending request to {agent_pod['entity_extractor'].agent_name}...')
    response_content = agent_pod["entity_extractor"].get_response(entity_extractor_message).choices[0].message.content
    logger.llm(f'Sending request to {agent_pod['entity_extractor'].agent_name} executed')
    
    extracted_entities_steps_json = json.loads(response_content)
    
    operations = [
        Operation(step=step['step'], operation=step['op'], arg_1=step['arg1'], arg_2=step['arg2'])
        for step in extracted_entities_steps_json['steps']
    ]
    
    logger.info(f"Operations steps to be executed: {len(operations)}")
    logger.info(f"Operations to be executed: {operations}")
    
    try:
        logger.info("Attempting to execute operation chain...")
        executor = OperationChainExecutor(operations)
        result = executor.execute()
        logger.info("Operation chain executed successfully")
    except Exception as e:
        # Log the exception with an error message
        logger.error(f"Failed to execute operation chain: {e}")
        
        logger.exception("Exception occurred")
        
        # Set the result to indicate failure
        result = "Could not execute operation chain"


    query_response = QueryResponse(
        question=query_request.message,
        answer=result,
        operations=operations,
        steps=len(operations),
        input_tokens=100,
        ouput_tokens=100,
        latency=100.0,
        status="Success"
    )
    
    return query_response

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
    