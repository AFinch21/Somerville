from pydantic import BaseModel
from pydantic import UUID4
from typing import Optional

# Define a Pydantic model for the response payload
class ResponseModel(BaseModel):
    message: str
    status: str

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
    
class Operation(BaseModel):
    step: int
    operation: str
    arg_1: str
    arg_2: str