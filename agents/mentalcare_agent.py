import os
from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent
from plugins.user_profile_query_plugin import UserProfileQueryPlugin
from plugins.mentalcare_plugin import MentalCarePlugin

load_dotenv()
AGENT_ID = os.getenv('MENTAL_CARE_ASSISTANT')

async def create_mentalcare_agent():
    creds = DefaultAzureCredential()
    client = AzureAIAgent.create_client(credential=creds)
    mentalcare_plugin = MentalCarePlugin()
    agent_definition = await client.agents.get_agent(agent_id=AGENT_ID)
    agent = AzureAIAgent(client=client, definition=agent_definition, plugins=[mentalcare_plugin, UserProfileQueryPlugin()])
    return agent, client, creds
"""
MentalCareAgent: An AI assistant for mental well-being support.

Core Functions:
1. Assessment:
    - Greets user and evaluates emotional state
    - Uses open-ended questions about feelings, stress, and sleep
    - Follows up for clarity when needed

2. Music Recommendations:
    - get_peaceful_music: For stress and anxiety
    - get_healing_music: For sadness and low mood
    - get_gym_music: For energy and motivation

Example Questions:
- "How are you feeling today?"
- "What's your current stress level?"
- "How has your sleep been recently?"
"""
