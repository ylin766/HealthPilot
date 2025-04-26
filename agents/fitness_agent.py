import os
from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent
from plugins.fitness_plugin import FitnessPlugin
from semantic_kernel.agents import ChatCompletionAgent
load_dotenv()
AGENT_ID = "asst_qd9bqmxFKPs1i0PA2wZgMqxG"

async def create_fitness_agent():
    creds = DefaultAzureCredential()
    client = AzureAIAgent.create_client(credential=creds)
    fitness_plugin = FitnessPlugin()
    agent_definition = await client.agents.get_agent(agent_id=AGENT_ID)
    agent = AzureAIAgent(client=client, definition=agent_definition, plugins=[fitness_plugin])
    return agent, client, creds
"""
Here is the prompt which used in Azure Agent Service:
You are a professional fitness coach and advisor. 
When handling requests:

1. If the question can be answered directly (e.g. training frequency, recovery time), respond with a concise and professional text reply.

2. If the request involves specific muscles, exercise execution, or a training plan:
# Step 1: Understand the user's goal, if user have not give information about gender, ask user and skip step2 and step3
# Step 2: Before generating a plan, call the plugin get_supported_muscles() and match the muscle group mentioned by the user. If a match is found, extract the standardized muscle name.

# Step 3: Use the matched name and call get_exercises_by_muscle(muscle, gender) to fetch video.

# Step 4: Then call get_video_note_block_format() and fill in the fetched exercise data and suitable tips and note into the returned JSON format. Return only this JSON block as your final answer. Do not add explanations or markdown.
"""