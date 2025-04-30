from semantic_kernel.agents import ChatCompletionAgent
from services.openai_service import get_openai_service
from plugins.health_manager_plugin import HealthManagerPlugin
from agents.nutrition_agent import create_nutrition_agent
from agents.fitness_agent import create_fitness_agent
from agents.mentalcare_agent import create_mentalcare_agent
from plugins.user_profile_query_plugin import UserProfileQueryPlugin

async def create_health_manager(
    kernel,
    nutrition_agent, nutrition_thread,
    fitness_agent, fitness_thread,
    mentalcare_agent, mentalcare_thread
):
    health_manager_plugin = HealthManagerPlugin(
        nutrition_agent=nutrition_agent, nutrition_thread=nutrition_thread,
        fitness_agent=fitness_agent, fitness_thread=fitness_thread,
        mentalcare_agent=mentalcare_agent, mentalcare_thread=mentalcare_thread
    )

    query_plugin = UserProfileQueryPlugin()

    return ChatCompletionAgent(
        kernel=kernel,
        name="HealthManager",
        plugins = [health_manager_plugin, query_plugin],
        instructions="""
        You are HealthManager, a helpful health assistant.

Your responsibilities:
1. Read the full conversation and the latest user message carefully.
2. If the user provides personal health-related information (like age, height, or weight), use the appropriate plugin to save or update the user's profile.
3. If the user asks for support related to fitness, diet/nutrition, or mental health, summarize the need and generate a clear, specific prompt to assist.
4. Then, choose the right assistant (Fitness, Nutrition, or MentalCare) and forward the prompt using the correct plugin.
5. If the message is general or unrelated to those areas, respond yourself with a brief helpful reply.

Note:
- The plugin you trigger will handle the next response.
- You do not need to explain plugin behavior or outputs to the user.


"""
    )
