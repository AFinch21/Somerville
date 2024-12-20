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
                if data[item]["question"] == question:
                    question_data = ConvFinQADataQuestion(
                        id=str(data[item]["id"]),
                        company=str(data[item]["company"]),
                        year=str(data[item]["year"]),
                        filename=str(data[item]["filename"]),
                        pre_text=str(data[item]["pre_text"]),
                        post_text=str(data[item]["post_text"]),
                        table_ori=str(data[item]["table_ori"]),
                        question=data[item]["question"],
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
                    steps_num=row[9],
                    program=row[10],
                    exe_answer=row[12],
                )
                questions.append(question)
    else:
        
        with open(file_path, "r") as f:
            data = json.load(f)
            
            for item in data:
                question = ConvFinQADataEval(
                    id=str(data[item]["id"]),
                    company=str(data[item]["company"]),
                    year=str(data[item]["year"]),
                    filename=str(data[item]["filename"]),
                    pre_text=str(data[item]["pre_text"]),
                    post_text=str(data[item]["post_text"]),
                    table_ori=str(data[item]["table_ori"]),
                    question=str(data[item]["question"]),
                    steps=str(data[item]["steps"]),
                    steps_num=str(data[item]["step_num"]),
                    program=str(data[item]["program"]),
                    exe_answer=str(data[item]["exe_answer"]),
                )
                questions.append(question)
    
    return questions

def get_evaluation_data(engine, n, file_path, database=True, minimum_steps=0):
    questions = []
    if database:
        # Use the database logic and filter by minimum_steps
        stmt = (
            select(ConvFinQAData)
            .where(ConvFinQAData.steps_num >= minimum_steps)  # Ensure steps_num meets the condition
            .order_by(func.random())  # Randomize results
            .limit(n)  # Limit the number of records
        )

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
                    steps_num=row[9],
                    program=row[10],
                    exe_answer=row[12],
                )
                questions.append(question)

    else:  # When reading from a file
        with open(file_path, "r") as f:
            data = json.load(f)
            # Randomly select `n` items from the loaded data
            if isinstance(data, dict):
                sampled_keys = random.sample(list(data.keys()), len(data))
                sampled_items = [data[key] for key in sampled_keys]
            else:
                sampled_items = data

            # Filter the sampled items for minimum_steps and then randomize n
            filtered_items = [
                item for item in sampled_items if int(item["step_num"]) >= minimum_steps
            ]
            if len(filtered_items) < n:
                raise ValueError(
                    f"Not enough items in the file meet the 'minimum_steps'={minimum_steps} condition."
                )
            selected_items = random.sample(filtered_items, n)
            
            # Map the filtered and selected items to ConvFinQADataEval
            for item in selected_items:
                question = ConvFinQADataEval(
                    id=str(item["id"]),
                    company=str(item["company"]),
                    year=str(item["year"]),
                    filename=str(item["filename"]),
                    pre_text=str(item["pre_text"]),
                    post_text=str(item["post_text"]),
                    table_ori=str(item["table_ori"]),
                    question=str(item["question"]),
                    steps=str(item["steps"]),
                    steps_num=str(item["step_num"]),
                    program=str(item["program"]),
                    exe_answer=str(item["exe_answer"]),
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
                    steps_num=str(records[row]["step_num"]),
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