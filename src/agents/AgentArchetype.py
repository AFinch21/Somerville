from openai import OpenAI
import openai
from model.Model import BaseAgent, Prompt, AgentDetails
from database.Operations import get_prompts, get_agents
from database.Database import get_db

class Agent:
    def __init__(self, agent_id, agent_name, api_key):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.api_key = api_key
        self.client = self.get_client()
        self.database = get_db()
        self.system_prompt = get_prompts(self.database, agent_id).system_prompt
        self.user_prompt = get_prompts(self.database, agent_id).user_prompt


    def get_client(self):
        # Instantiate OpenAI client using the provided API key
        client = OpenAI(api_key=self.api_key)
        return client

    def get_agent_details(self) -> AgentDetails:
        # Ensure get_system_prompt and get_user_prompt are accessible
        details = AgentDetails(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            api_key=self.api_key,
            system_prompt=self.system_prompt,
            user_prompt=self.user_prompt  # Define or pass the correct user_prompt
        )
        return details
    
    
    def build_user_prompt(self, user_message: str) -> str:

        # Formatting the prompt string with the given user message
        # Here, 'user_message=user_message' is key=value where key must match the placeholder in the string
        formatted_prompt = self.user_prompt.format(user_message=user_message)
        
        return formatted_prompt
    
    # def get_tools(self) -> list:
    #     # Define or format the user prompt appropriately
    #     return [openai.pydantic_function_tool(TaskManagerClassification),]
    
    def create_messages(self, agent_input) -> dict:
        
        messages=[
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.build_user_prompt(agent_input)}
        ]
        
        return messages
    
    def get_response(self, agent_input):
        
        messages = self.create_messages(agent_input)
        # tools = self.get_tools()
        tools = []
        json = True
        
        response = self.call_llm(
            messages=messages,
            json_mode=json,
            tools=tools,
        )
        
        return response
    
    def call_llm(self, messages, json_mode, tools: list = []):
        # Ensure client is initialized before calling this method
        
        # If we have tools in the list, we ruun a tool call

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools = tools if len(tools) > 0 else None,
                response_format= { "type": "json_object" } if json_mode else None
            )
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        return completion