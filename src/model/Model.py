from pydantic import BaseModel
from pydantic import UUID4
from typing import Optional, Union

# Define a Pydantic model for the response payload
class QueryRequest(BaseModel):
    message: str
    max_retries: int
    status: str
    
class EvaluationRequest(BaseModel):
    n_questions: int
    min_steps: int
    max_retries: int
    status: str
    
class Operation(BaseModel):
    step: int
    operation: str
    arg_1: Union[float, str]
    arg_2: Union[float, str]
    
class QueryResponse(BaseModel):
    question: str
    answer: Union[float, str]
    operation_arguments: list[Operation]
    operations: list[Operation]
    steps: int
    input_tokens: int
    ouput_tokens: int
    latency: float
    status: str
    
class EvaluationResponse(BaseModel):
    question: str
    answer: Union[float, str]
    predicted_operations: list[Operation]
    predicted_steps: int
    input_tokens: int
    ouput_tokens: int
    latency: float
    true_steps: int
    true_program: str
    true_answer: float
    
class EvaluationSummary(BaseModel):
    responses: list[EvaluationResponse]
    num_eval_questions: int
    num_answered_questions: int
    num_correct_answers: int
    answer_accuracy: float
    step_accuracy: float
    average_latency: float
    max_latency: float
    min_latency: float

# Define a Pydantic model for the evaluation payload
class EvaluationModel(BaseModel):
    score: int
    feedback: str
    
class BaseAgent(BaseModel):
    agent_id: UUID4
    agent_name: str
    api_key: str

class Prompt(BaseModel):
    agent_id: UUID4
    system_prompt: str
    user_prompt: str
    
class AgentDetails(BaseModel):
    agent_id: UUID4
    agent_name: str
    api_key: str
    system_prompt: str
    user_prompt: str
    
    
class ConvFinQADataSchema(BaseModel):
    id: str
    company: Optional[str] = None
    year: Optional[str] = None
    filename: Optional[str] = None
    pre_text: Optional[str] = None
    post_text: Optional[str] = None
    table_ori: Optional[str] = None
    question: Optional[str] = None
    steps: Optional[str] = None
    steps: Optional[int] = None
    program: Optional[str] = None
    answer: Optional[str] = None
    exe_answer: Optional[float] = None
    str_exe_answer: Optional[str] = None

    class Config:
        orm_mode = True
        
class ConvFinQADataQuestion(BaseModel):
    id: str
    company: Optional[str] = None
    year: Optional[str] = None
    filename: Optional[str] = None
    pre_text: Optional[str] = None
    post_text: Optional[str] = None
    table_ori: Optional[str] = None
    question: Optional[str] = None
    
class ConvFinQADataEval(BaseModel):
    id: str
    company: Optional[str] = None
    year: Optional[str] = None
    filename: Optional[str] = None
    pre_text: Optional[str] = None
    post_text: Optional[str] = None
    table_ori: Optional[str] = None
    question: Optional[str] = None
    steps: Optional[str] = None
    steps_num: Optional[int] = None
    program: Optional[str] = None
    exe_answer: float
    