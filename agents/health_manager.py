from semantic_kernel.agents import ChatCompletionAgent
from services.openai_service import get_openai_service
from plugins.task_dispatcher_plugin import TaskDispatcherPlugin
from agents.nutrition_agent import create_nutrition_agent
from agents.fitness_agent import create_fitness_agent
from agents.mentalcare_agent import create_mentalcare_agent

async def create_health_manager(
    kernel,
    nutrition_agent, nutrition_thread,
    fitness_agent, fitness_thread,
    mentalcare_agent, mentalcare_thread
):
    dispatcher_plugin = TaskDispatcherPlugin(
        nutrition_agent, nutrition_thread,
        fitness_agent, fitness_thread,
        mentalcare_agent, mentalcare_thread
    )
    return ChatCompletionAgent(
        kernel=kernel,
        name="HealthManager",
        plugins = [dispatcher_plugin],
        instructions="""
        You are HealthManager, an agent that routes user requests.

If the message involves fitness, diet, or mental health, generate proper prompts (including the message and relevant stored health info), and delegate to one or more corresponding agents as needed.
Otherwise, answer directly.
Also:

Store any health info users provide (e.g., age, goals).
Decide whether to continue with current agents or switch based on user input.

"""
    )
