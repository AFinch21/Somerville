from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Boolean, Column, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from logger.Logger import get_logger
from typing import List

logger = get_logger()
Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"
    
    agent_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    agent_name: Mapped[str] = mapped_column(String)
    api_key: Mapped[str] = mapped_column(String)

    # One-to-one relationship
    prompt: Mapped['AgentPrompts'] = relationship("AgentPrompts", back_populates="agent", uselist=False)

    # One-to-many relationship
    requests: Mapped[List['ResponseModel']] = relationship("ResponseModel", back_populates="agent")

    def __repr__(self) -> str:
        return f"Agent(agent_id={self.agent_id!r}, agent_name={self.agent_name!r})"

class AgentPrompts(Base):
    __tablename__ = "agent_prompts"
    
    agent_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('agents.agent_id'), primary_key=True)
    system_prompt: Mapped[str] = mapped_column(String)
    user_prompt: Mapped[str] = mapped_column(String)
    json_mode: Mapped[bool] = mapped_column(Boolean)

    # Relationship back to Agent
    agent: Mapped[Agent] = relationship("Agent", back_populates="prompt")

    def __repr__(self) -> str:
        return f"AgentPrompts(agent_id={self.agent_id!r}, system_prompt={self.system_prompt!r}, user_prompt={self.user_prompt!r})"

class ResponseModel(Base):
    __tablename__ = "user_requests"
    
    request_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    agent_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('agents.agent_id'))
    message: Mapped[str] = mapped_column(String)

    # Many-to-one relationship to Agent
    agent: Mapped[Agent] = relationship("Agent", back_populates="requests")

    def __repr__(self) -> str:
        return f"ResponseModel(request_id={self.request_id!r}, agent_id={self.agent_id!r}, user_input={self.user_input!r})"
    
    
class ConvFinQAData(Base):
    __tablename__ = 'convfinqa_data'  # replace with your actual table name

    # Define columns
    id = Column(String, primary_key=True)  # Assuming 'id' is unique or can be primary key
    company = Column(String)
    year = Column(String)
    filename = Column(String)
    pre_text = Column(String)
    post_text = Column(String)
    table_ori = Column(String)
    question = Column(String)
    steps = Column(String)
    steps_num = Column(Integer)
    program = Column(String)
    answer = Column(String)
    exe_answer = Column(Float)
    str_exe_answer = Column(String) 


# Helper function to create the database connection and tables
def init_db(engine):
    try:
        Base.metadata.create_all(engine)
        logger.info("Database schema created successfully.")
        return engine
    except Exception as e:  
        logger.warning(f"Table creation failed - please check datafile. Error: {e}")

if __name__ == "__main__":
    init_db()