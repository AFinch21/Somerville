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
from utilities.AppStartup import initialize_database, load_agents
from logger.Logger import get_logger
import ast

app = FastAPI()

# Get logger
logger = get_logger()

# Define our local data storage
use_database= True if os.environ.get('USE_DATABASE') == 'yes' else False
json_file_path = "data/ConvFincQA_data.json"
agent_file_path = "data/agents.json"
agent_prompt_file_path = "data/prompts.json"

# Run this startup wrapper to get everything set up
try:
    # Step 1: Initialize the database
    db = initialize_database(json_file_path, agent_file_path, agent_prompt_file_path, use_database)
    
    # Step 2: Load and initialize agents
    agent_pod = load_agents(db, use_database, agent_file_path, agent_prompt_file_path)

    if agent_pod:
        logger.info("Application setup complete.")
    else:
        logger.warning("Application setup incomplete. Check previous errors.")

except Exception as error:
    logger.error(f"Application failed to load. Error: {error}")

 
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
    
    evaluation_set = get_evaluation_data(agent_pod, eval_request.n_questions, json_file_path, use_database)
    
    responses = []
    
    for eval_question in evaluation_set:
        query_request = QueryRequest(
            message=eval_question.question,
            max_retries=eval_request.max_retries,
            status="Success"
        )
        try:
            result = execute_agent_workflow(db, agent_pod, query_request, json_file_path, use_database)
            evaluation_response = EvaluationResponse(
                question=result.question,
                answer=result.answer,
                predicted_operations=result.operations,
                predicted_steps=len(result.operations),
                input_tokens=result.input_tokens,
                ouput_tokens=result.ouput_tokens,
                latency=result.latency,
                true_steps=len(ast.literal_eval(eval_question.steps)),
                true_program=eval_question.program,
                true_answer=eval_question.exe_answer
            )
        except Exception as error:
            logger.error(f"Could not formulate response. Error: {error}")
            evaluation_response = EvaluationResponse(
                question=result.question,
                answer=r"Error in Agent workflow",
                predicted_operations=[],
                predicted_steps=0,
                input_tokens=100,
                ouput_tokens=100,
                latency=result.latency,
                true_steps=len(ast.literal_eval(eval_question.steps)),
                true_program=eval_question.program,
                true_answer=eval_question.exe_answer
            )

        responses.append(evaluation_response)
    
    evaluation_summary = process_evaluation_run(responses)
    

    return evaluation_summary

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    