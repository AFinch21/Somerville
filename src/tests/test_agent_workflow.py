import unittest
from unittest.mock import patch, MagicMock
from agents.AgentArchetype import Agent  
import os
from model.Model import BaseAgent, QueryRequest
from agents.AgentInitialisation import iniatialise_agents
from utilities.AgentWorkflow import execute_agent_workflow
from utilities.AppStartup import get_agents, iniatialise_agents
import json


agent = Agent(
        agent_id = "33ccb890-1673-4110-83fc-cf7fda74a01a",
        agent_name="program_builder",
        api_key=str(os.environ.get('OPENAI_API_KEY')),
        use_database=False,
        local_prompts="src/data/prompts.json",
    )

def test_initialise_agents():
    agent_list = [
        BaseAgent(
            agent_id="33ccb890-1673-4110-83fc-cf7fda74a01a",
            agent_name="program_builder",
            api_key=str(os.environ.get('OPENAI_API_KEY')),  # Replace API key
        )
    ]
    
    agent_prompt_file_path = "src/data/prompts.json"
    
    agents = iniatialise_agents(agent_list, False, agent_prompt_file_path)
    
    assert len(agents) == 1
    assert str(agents["program_builder"].agent_id) == "33ccb890-1673-4110-83fc-cf7fda74a01a"

def test_get_agent_details():
    
    agent_details = agent.get_agent_details()
    
    assert str(agent_details.agent_id) == "33ccb890-1673-4110-83fc-cf7fda74a01a"
    assert agent_details.agent_name == "program_builder"
    

def test_get_response():
    
    response = agent.get_response("what was the percentage change in the net cash from operating activities from 2008 to 2009").choices[0].message.content

    parsed = json.loads(response)  # Attempt to parse
    assert (isinstance(parsed, dict)) == True
    
def test_execute_agent_workflow():
    
    request = QueryRequest(
        message = "what was the percentage change in the net cash from operating activities from 2008 to 2009",
        max_retries=3,
        status = "success"
    )
    agent_data = get_agents(None, "src/data/agents.json", False)
    agent_pod = iniatialise_agents(agent_data, False, "src/data/prompts.json")


    
    query_response = execute_agent_workflow(None, agent_pod, request, "src/data/ConvFincQA_data.json", False)
    
    assert query_response.question == request.message
    
    assert query_response.status == "Success"
    