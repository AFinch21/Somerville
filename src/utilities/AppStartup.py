
from database.Database import get_db
from database.ORM import init_db
from database.Operations import get_agents, upload_input_data, upload_agent_data, upload_prompt_data
from agents.AgentArchetype import Agent
from agents.AgentInitialisation import iniatialise_agents
from logger.Logger import get_logger

logger = get_logger()

def initialize_database(json_file_path, agent_file_path, agent_prompt_file_path, use_database):
    """
    Initialize and populate the database, if required.
    """
    try:
        if use_database:
            db = get_db()
            init_db(db)
            upload_input_data(db, json_file_path)
            upload_agent_data(db, agent_file_path)
            upload_prompt_data(db, agent_prompt_file_path)
            logger.info(f"Database enabled. Data upload complete.")
        else:
            db = None
            logger.info("Database disabled. Using local JSON files.")
        return db
    except Exception as error:
        logger.warning(f"Data upload failed. Please check your data files. Error: {error}")
        return None

def load_agents(db, use_database, agent_file_path, agent_prompt_file_path):
    """
    Load agents and initialize them from the database or files.
    """
    try:
        agent_data = get_agents(db, agent_file_path, use_database)
        agent_pod = iniatialise_agents(agent_data, use_database, agent_prompt_file_path)
        logger.info("Agent initialization complete.")
        return agent_pod
    except Exception as error:
        logger.warning(f"Agent loading failed. Please check your data files. Error: {error}")
        return None
