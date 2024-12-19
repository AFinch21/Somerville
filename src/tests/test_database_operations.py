import pytest
from unittest.mock import MagicMock, patch
from utilities.AgentWorkflow import execute_agent_workflow
from model.Model import QueryRequest, QueryResponse, Operation
from database.Operations import get_question_data, get_all_question_data, get_evaluation_data, get_agents, upload_input_data, upload_prompt_data, upload_agent_data, get_prompts
from model.Model import ConvFinQADataQuestion, BaseAgent, Prompt
import pytest
from unittest.mock import patch, mock_open
import json
import uuid

def test_get_question_data():
    
    engine = None
    question = "what was the percentage change in the net cash from operating activities from 2008 to 2009"
    file_path = "src/data/ConvFincQA_data.json"
    database=False
        
    dummy_data = ConvFinQADataQuestion(
        id="Single_JKHY/2009/page_28.pdf-3",
        company="JKHY",
        year="2009",
        filename="UPS/2009/page_33.pdf",
        pre_text="",
        post_text="['.']",
        table_ori="",
        question="what was the percentage change in the net cash from operating activities from 2008 to 2009"
    )
    result = get_question_data(engine, question, file_path, database)
    assert result.id == dummy_data.id
    assert result.company == dummy_data.company
    assert result.year == dummy_data.year


def test_get_all_question_data():
    
    engine = None
    file_path = "src/data/ConvFincQA_data.json"
    database=False
        
    result = get_all_question_data(engine, file_path, database)
    assert len(result) < 3036

def test_get_evaluation_data():
    
    engine = None
    n = 50
    file_path = "src/data/ConvFincQA_data.json"
    database=False
        
    result = get_evaluation_data(engine, n, file_path, database)
    assert len(result) == 50
    
def test_get_agents():
    engine = None
    file_path = "src/data/agents.json"
    database = False


    result = get_agents(engine, file_path, database)
    
    assert len(result) == 2
    assert result[0].agent_name == "program_builder"

def test_get_prompts():
    engine = None
    agent_id = "33ccb890-1673-4110-83fc-cf7fda74a01a"
    file_path = "src/data/prompts.json"
    database = False


    result = get_prompts(engine, agent_id, database, file_path)
    

    assert result.user_prompt == "Here is the question and the report data:\n\n{user_message}"
