from database.ORM import Agent, AgentPrompts, ResponseModel, ConvFinQAData
from model.Model import Prompt, BaseAgent, ConvFinQADataQuestion, ConvFinQADataEval
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import select, func
from logger.Logger import get_logger
import os
import json
import random

Base = declarative_base()
# Get logger
logger = get_logger()

#GET DATA FUNCTIONS

def get_question_data(engine, question, file_path, database=True):
    if database:
        stmt = select(ConvFinQAData).where(ConvFinQAData.question == question)
        
        with engine.connect() as conn:
            for row in conn.execute(stmt):
                question_data = ConvFinQADataQuestion(
                    id=row[0],
                    company=row[1],
                    year=row[2],
                    filename=row[3],
                    pre_tex=row[4],
                    post_text=row[5],
                    table_ori=row[6],
                    question=row[7],
                )
                return question_data
    else:        
        with open(file_path, "r") as f:
            data = json.load(f)
            
            for item in data:
                if item["question"] == question:
                    question_data = ConvFinQADataQuestion(
                        id=item["id"],
                        company=item["company"],
                        year=item["year"],
                        filename=item["filename"],
                        pre_tex=item["pre_tex"],
                        post_text=item["post_text"],
                        table_ori=item["table_ori"],
                        question=item["question"],
                    )
                    return question_data
    
    return None 

def get_all_question_data(engine, file_path, database=True):
    questions = []

    if database:
        # Use the database logic
        stmt = select(ConvFinQAData)
        
        with engine.connect() as conn:
            for row in conn.execute(stmt):
                question = ConvFinQADataEval(
                    id=row[0],
                    company=row[1],
                    year=row[2],
                    filename=row[3],
                    pre_tex=row[4],
                    post_text=row[5],
                    table_ori=row[6],
                    question=row[7],
                    steps=row[8],
                    program=row[9],
                    exe_answer=row[11],
                )
                questions.append(question)
    else:
        
        with open(file_path, "r") as f:
            data = json.load(f)
            
            for item in data:
                question = ConvFinQADataEval(
                    id=item["id"],
                    company=item["company"],
                    year=item["year"],
                    filename=item["filename"],
                    pre_tex=item["pre_tex"],
                    post_text=item["post_text"],
                    table_ori=item["table_ori"],
                    question=item["question"],
                    steps=item["steps"],
                    program=item["program"],
                    exe_answer=item["exe_answer"],
                )
                questions.append(question)
    
    return questions

def get_evaluation_data(engine, n, file_path, database=True):
    questions = []

    if database:
        # Use the database logic
        stmt = select(ConvFinQAData).order_by(func.random()).limit(n)
        
        with engine.connect() as conn:
            result = conn.execute(stmt)
            
            for row in result:
                question = ConvFinQADataEval(
                    id=row[0],
                    company=row[1],
                    year=row[2],
                    filename=row[3],
                    pre_tex=row[4],
                    post_text=row[5],
                    table_ori=row[6],
                    question=row[7],
                    steps=row[8],
                    program=row[9],
                    exe_answer=row[11],
                )
                questions.append(question)
    else:
                
        with open(file_path, "r") as f:
            data = json.load(f)
            
            # Randomly select `n` items from the loaded data
            sampled_items = random.sample(data, n)
            
            for item in sampled_items:
                question = ConvFinQADataEval(
                    id=item["id"],
                    company=item["company"],
                    year=item["year"],
                    filename=item["filename"],
                    pre_tex=item["pre_tex"],
                    post_text=item["post_text"],
                    table_ori=item["table_ori"],
                    question=item["question"],
                    steps=item["steps"],
                    program=item["program"],
                    exe_answer=item["exe_answer"],
                )
                questions.append(question)
    
    return questions


def get_agents(engine, file_path, database=True):
    agents = []
    
    if database:
        # Use the existing database logic
        stmt = select(Agent)
        
        with engine.connect() as conn:
            for row in conn.execute(stmt):
                agent = BaseAgent(
                    agent_id=row[0],
                    agent_name=row[1],
                    api_key=row[2],
                )
                agents.append(agent)
    else:
        # Load the JSON file
        with open(file_path, "r") as f:
            data = json.load(f)
            
            for item in data:
                agent = BaseAgent(
                    agent_id=item["agent_id"],
                    agent_name=item["agent_name"],
                    api_key=str(os.environ.get('OPENAI_API_KEY')),  # Replace API key
                )
                agents.append(agent)
    
    return agents

def get_prompts(engine, agent_id, database, local_prompts):
    if database:
        stmt = select(AgentPrompts).where(AgentPrompts.agent_id == agent_id)
        
        with engine.connect() as conn:
            for row in conn.execute(stmt):
                prompt = Prompt(
                    agent_id=row[0],
                    system_prompt=row[1],
                    user_prompt=row[2],
                )
                return prompt
    else:        
        with open(local_prompts, "r") as f:
            data = json.load(f)
            for item in data:
                if item["agent_id"] == str(agent_id):
                    prompt = Prompt(
                        agent_id=item["agent_id"],
                        system_prompt=item["system_prompt"],
                        user_prompt=item["user_prompt"],
                    )
                    return prompt
    
    return None


### UPLOAD FUNCTIONS

        
def upload_input_data(engine, json_file_path):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        Base.metadata.create_all(engine)
        
        with open(json_file_path, 'r') as file:
            records = json.load(file)
        
        data_objects = []
        
        for row in records:
            
            existing_record = session.query(ConvFinQAData).filter_by(id=records[row]['id']).first()
            
            if not existing_record:
                logger.info(f"Record {records[row]['id']} not found in DB - uploading...")
                data_object = ConvFinQAData(
                    id=records[row]['id'],
                    company=str(records[row]['company']),
                    year=str(records[row]['year']),
                    filename=str(records[row]['filename']),
                    pre_text=str(records[row]['pre_text']),
                    post_text=str(records[row]['post_text']),
                    table_ori=str(records[row]['table_ori']),
                    question=str(records[row]['question']),
                    steps=str(records[row]['steps']),
                    program=str(records[row]['program']),
                    answer=str(records[row]['answer']),
                    exe_answer=str(records[row]['exe_answer'])
                )
                data_objects.append(data_object)
        
        session.add_all(data_objects)
        session.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def upload_prompt_data(engine, json_file_path):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        Base.metadata.create_all(engine)

        with open(json_file_path, 'r') as file:
            records = json.load(file) 

        data_objects = []
        for record in records:  
            existing_record = session.query(AgentPrompts).filter_by(agent_id=record['agent_id']).first()
            
            if not existing_record:
                logger.info(f"Agent {record['agent_id']} not found in DB - uploading...")
                data_object = AgentPrompts(
                    agent_id=record['agent_id'],
                    system_prompt=str(record['system_prompt']),
                    user_prompt=str(record['user_prompt']),
                    json_mode=bool(record['json_mode'])
                )
                data_objects.append(data_object)

        session.add_all(data_objects)
        session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()
        
def upload_agent_data(engine, json_file_path):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        Base.metadata.create_all(engine)

        with open(json_file_path, 'r') as file:
            records = json.load(file)  #

        data_objects = []
        for record in records:  
            existing_record = session.query(Agent).filter_by(agent_id=record['agent_id']).first()
            
            if not existing_record:
                logger.info(f"Agent {record['agent_name']} not found in DB - uploading...")
                data_object = Agent(
                    agent_id=record['agent_id'],
                    agent_name=str(record['agent_name']),
                    api_key=str(os.environ.get('OPENAI_API_KEY'))
                )
                data_objects.append(data_object)

        session.add_all(data_objects)
        session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()