from database.ORM import Agent, AgentPrompts, UserRequest
from model.Model import Prompt, BaseAgent
from sqlalchemy import select

def get_question_data(engine):
    
    # stmt = select(Agent)

    # agents = []
    
    # with engine.connect() as conn:
    #     for row in conn.execute(stmt):
            
    #         agent = BaseAgent(
    #             agent_id = row[0],
    #             agent_name= row[1],
    #             api_key= row[2],
    #         )
            
    #         agents.append(agent)
    
    # return agents
    pass

def get_evaluation_stats(engine, agent_id):
    # stmt = select(AgentPrompts).where(AgentPrompts.agent_id == agent_id)

    
    
    # with engine.connect() as conn:
    #     for row in conn.execute(stmt):
    #         prompt = Prompt(
    #             agent_id = row[0],
    #             system_prompt= row[1],
    #             user_prompt= row[2]
    #         )
    
    # return prompt
    pass

def get_agents(engine):
    
    stmt = select(Agent)

    agents = []
    
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            
            agent = BaseAgent(
                agent_id = row[0],
                agent_name= row[1],
                api_key= row[2],
            )
            
            agents.append(agent)
    
    return agents

def get_prompts(engine, agent_id):
    stmt = select(AgentPrompts).where(AgentPrompts.agent_id == agent_id)

    
    
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            prompt = Prompt(
                agent_id = row[0],
                system_prompt= row[1],
                user_prompt= row[2]
            )
    
    return prompt