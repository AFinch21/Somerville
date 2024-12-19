from fastapi import FastAPI
import os
from model.Model import QueryRequest, Operation, QueryResponse, EvaluationResponse, EvaluationSummary, EvaluationRequest
from database.Database import get_db
from database.ORM import init_db
from database.Operations import get_agents, upload_input_data, get_evaluation_data, get_all_question_data, upload_agent_data, upload_prompt_data
from agents.AgentArchetype import Agent
from agents.AgentInitialisation import iniatialise_agents
from utilities.PromptTemplates import entity_extraction_message, operation_chains_message
from utilities.ProcessEvalResults import process_evaluation_run
from utilities.AgentWorkflow import execute_agent_workflow
from logger.Logger import get_logger

app = FastAPI()

# Get logger
logger = get_logger()

# Define our local data storage
use_database= os.environ.get('USE_DATABASE')
json_file_path = "data/ConvFincQA_data.json"
agent_file_path = "data/agents.json"
agent_prompt_file_path = "data/prompts.json"

try:
    try:
        # If you ant to use a SQL DB - initialise our database
        if use_database:
            db = get_db()
            init_db(db)
            upload_input_data(db, json_file_path)
            upload_agent_data(db, agent_file_path)
            upload_prompt_data(db, agent_prompt_file_path)
            logger.info(f"Database use set to {use_database} - Data Upload Complete")
        else:
            db = None
            logger.info(f"Database use set to {use_database} - using local JSONs")
    except Exception as e:  
        logger.warning(f"Data Upload failed - please check datafile. Error: {e}")

    # Go to our database and grab our agents and initialise them
    try:
        agent_data = get_agents(db, agent_file_path, False)
        agent_pod = iniatialise_agents(agent_data, False, agent_prompt_file_path)
        logger.info("Application set up complete")
    except Exception as e:  
        logger.warning(f"Agent load failed - please check datafile. Error: {e}")
except Exception as e:  
        logger.error(f"Application load failed - Error: {e}")
 

@app.get("/")
async def root():
    return {"Hello World"}

@app.get("/get_question_list")
async def get_question_list():
    question_metadata = get_all_question_data(db, json_file_path, use_database)
    return question_metadata


@app.post("/answer_question", response_model=QueryResponse)
async def answer_question(query_request: QueryRequest):
    """
    Endpoint to process a question and execute a corresponding workflow.

    This endpoint receives a question encapsulated within a `QueryRequest` object
    and utilizes the `execute_agent_workflow` function to process the question,
    match it with relevant data, and perform necessary operations. Upon execution
    of the workflow, it returns a `QueryResponse` object that contains the result 
    of the operations, which is then sent back in the response to the requester.

    Parameters:
    - query_request: An instance of `QueryRequest` containing the question to be answered.

    Returns:
    - QueryResponse: An object containing the results of the processed query, including the
      answer, details of operations executed, and relevant metadata.
    """
    
    result = execute_agent_workflow(db, agent_pod, query_request, json_file_path, use_database)
    

    return result

@app.post("/get_evaluation", response_model=EvaluationSummary)
async def get_evaluation(eval_request: EvaluationRequest):
    """
    Endpoint to get an evaluation.
    """
    
    evaluation_set = get_evaluation_data(db, eval_request.n_questions, json_file_path, use_database)
    
    responses = []
    
    for eval_question in evaluation_set:
        query_request = QueryRequest(
            message=eval_question.question,
            max_retries=eval_request.max_retries,
            status="Success"
        )

        result = execute_agent_workflow(db, agent_pod, query_request)
        
        evaluation_response = EvaluationResponse(
            question=result.question,
            answer=result.answer,
            predicted_operations=result.operations,
            predicted_steps=len(result.operations),
            input_tokens=100,
            ouput_tokens=100,
            latency=100.0,
            true_steps=2,
            true_program=eval_question.program,
            true_answer=eval_question.exe_answer
        )

        responses.append(evaluation_response)
    
    evaluation_summary = process_evaluation_run(responses)
    

    return evaluation_summary

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    