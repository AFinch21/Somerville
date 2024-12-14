from agents.AgentArchetype import Agent

def iniatialise_agents(agent_list) -> list:
    
    new_agents = {}
    
    # We iterate over the agents data rows in the list and use the data to initialise an agent
    for a in agent_list:
        agent = Agent(
            agent_id=a.agent_id,
            agent_name=a.agent_name,
            api_key=a.api_key
        )
        new_agents[agent.agent_name] = agent
        
    return new_agents
        
        