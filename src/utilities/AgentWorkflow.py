import json
from model.Model import Operation
from database.Operations import get_question_data
from model.Model import QueryRequest, EvaluationModel, Operation, QueryResponse
from agents.AgentInitialisation import iniatialise_agents
from utilities.PromptTemplates import entity_extraction_message, operation_chains_message
from utilities.OperationExecutor import OperationChainExecutor
from logger.Logger import get_logger

# Get logger
logger = get_logger()

def execute_agent_workflow(db, agent_pod: list, query_request: QueryRequest) -> QueryResponse:
    """
    Executes a bespoke workflow to process and respond to a query request.

    This function orchestrates the workflow involving multiple agents to process a 
    query, extract entities, and execute a series of operations based on the results.
    It logs relevant information throughout the stages and handles any exceptions 
    that may occur during operation execution.

    Parameters:
    - db: Database connection object to fetch metadata related to the query.
    - agent_pod: A list of agents used for building programs and extracting entities.
    - query_request: An instance of QueryRequest containing the query message to be processed.

    Returns:
    - QueryResponse object containing the results of the executed operations, including
      the question, answer, details of the operations executed, and metadata like
      the number of input and output tokens, execution latency, and status.
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
    
    
    for attempt in range(1, query_request.max_retries + 1):
        try:
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
            
            break
            
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logger.error(f"Attempt {attempt} failed with error: {e}")
            if attempt == query_request.max_retries:
                logger.error("Max attempts reached. Returning dummy data.")
                DUMMY_OPERATIONS = [
                    {'step': 'dummy_step', 'op': 'dummy_op', 'arg1': 0.0, 'arg2': 0.0}
                ]
                query_response = QueryResponse(
                    question=query_request.message,
                    answer="Could not create operation chain",
                    operations=DUMMY_OPERATIONS,
                    steps=len(operations),
                    input_tokens=100,
                    ouput_tokens=100,
                    latency=100.0,
                    status="Success"
                )
                
                return query_response
            
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