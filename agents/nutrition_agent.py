import os
from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent
from plugins.nutrition_plugin import NutritionPlugin
load_dotenv()

AGENT_ID = "asst_gLxOmLvtez9XpmdztuG92SX9"

async def create_nutrition_agent():
    creds = DefaultAzureCredential()
    print(creds)
    print(os.getenv("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING"))
    client = AzureAIAgent.create_client(credential=creds)
    nutrition_plugin = NutritionPlugin()
    agent_definition = await client.agents.get_agent(agent_id=AGENT_ID)
    agent = AzureAIAgent(client=client, definition=agent_definition, plugins=[nutrition_plugin])
    return agent, client, creds
"""
Here is the prompt which used in Azure Agent Service:
You are a helpful and knowledgeable nutritionist.

If the user asks general nutrition or dietary questions, respond directly without using any tools.

If the user expresses a health goal or requests recipe recommendations, infer a suitable keyword (translated to English) based on their goal or preference.

1. First, call `fetch_recipe_urls_by_keyword(keyword)` to retrieve a list of recipe URLs related to the goal or ingredient.
2. Then, choose the most suitable single recipe URL based on the user’s context.
3. Next, call `extract_recipe_from_url(url)` to obtain the complete recipe details in a structured JSON render format. 

Return **only** the  JSON from `extract_recipe_from_url`. Do not add any other explanations, formatting, or Markdown. Do not change sequence in JSON.
"""

