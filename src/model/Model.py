from pydantic import BaseModel
from pydantic import UUID4
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
    
class TaskManagerClassification(BaseModel):
    category: str