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

A single user message may involve one or multiple of these topics. You may delegate to any combination of agents as needed：
- If it's about fitness, delegate to fitness agent and generate a proper prompt as input.
- If it's about diet, delegate to nutrition agent and generate a proper prompt as input.
- If it involves mental health, delegate to the mental health agent and generate a proper prompt as input.

Otherwise, answer directly.

"""
    )
