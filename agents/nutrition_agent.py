import os
from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent

load_dotenv()
AGENT_ID = "asst_0rrjAc6UTuFfeK2qvLIikprv"

async def create_nutrition_agent():
    creds = DefaultAzureCredential()
    client = AzureAIAgent.create_client(credential=creds)
    agent_definition = await client.agents.get_agent(agent_id=AGENT_ID)
    agent = AzureAIAgent(client=client, definition=agent_definition)
    return agent, client, creds


