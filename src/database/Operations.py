from database.ORM import Agent, AgentPrompts, ResponseModel, ConvFinQAData
from model.Model import Prompt, BaseAgent, ConvFinQADataQuestion, ConvFinQADataEval
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import select, func
import random
import json

Base = declarative_base()

def get_question_data(engine, question):
    
    stmt = select(ConvFinQAData).where(ConvFinQAData.question == question)

    
    
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            question = ConvFinQADataQuestion(
                id = row[0],
                company= row[1],
                year=row[2],
                filename= row[3],
                pre_tex=row[4],
                post_text= row[5],
                table_ori= row[6],
                question=row[7],
            )
    
    return question

def get_all_question_data(engine):
    stmt = select(ConvFinQAData)
    questions = []  
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            question = ConvFinQADataQuestion(
                id=row[0],
                company=row[1],
                year=row[2],
                filename=row[3],
                pre_tex=row[4],
                post_text=row[5],
                table_ori=row[6],
                question=row[7],
            )
            questions.append(question) 
    return questions  

def get_evaluation_data(engine, n):
    stmt = select(ConvFinQAData).order_by(func.random()).limit(n)

    with engine.connect() as conn:
        result = conn.execute(stmt)
        questions = []
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
                exe_answer=row[11]
            )
            questions.append(question)
    return questions


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