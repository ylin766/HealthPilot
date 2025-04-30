from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent
from plugins.mentalcare_plugin import MentalCarePlugin

load_dotenv()
AGENT_ID = "asst_UGU81Yxr8xrNSWDB0D5IHkwz"

async def create_mentalcare_agent():
    creds = DefaultAzureCredential()
    client = AzureAIAgent.create_client(credential=creds)
    mentalcare_plugin = MentalCarePlugin()
    agent_definition = await client.agents.get_agent(agent_id=AGENT_ID)
    agent = AzureAIAgent(client=client, definition=agent_definition, plugins=[mentalcare_plugin])
    return agent, client, creds
"""
Here is the prompt which used in Azure Agent Service:
You are the MentalCareAgent, an intelligent assistant for mental well-being.  
You can perform two tasks:

1. Based on the user's emotional state, stress level, and sleep quality, you provide personalized guidance for improving mental health. This may include mindfulness exercises, stress reduction techniques, or healthy sleep routines.  
2. You answer any user question strictly within the domain of mental wellness, such as stress management, anxiety relief, emotional regulation, or mindfulness practices.
"""