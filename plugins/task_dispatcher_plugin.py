from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread
import chainlit as cl
import chainlit.step

class TaskDispatcherPlugin:
    def __init__(
        self,
        nutrition_agent: AzureAIAgent, nutrition_thread: AzureAIAgentThread,
        fitness_agent: AzureAIAgent, fitness_thread: AzureAIAgentThread,
        mentalcare_agent: AzureAIAgent, mentalcare_thread: AzureAIAgentThread,
    ):
        self.nutrition_agent = nutrition_agent
        self.nutrition_thread = nutrition_thread
        self.fitness_agent = fitness_agent
        self.fitness_thread = fitness_thread
        self.mentalcare_agent = mentalcare_agent
        self.mentalcare_thread = mentalcare_thread

    @kernel_function(name="route_to_fitness", description="Route a fitness-related task.")
    async def route_to_fitness(self, message: str) -> str:
        print("🏋️ What manager send to fitness_agent：", message)
        async with cl.Step(name="Analyzing user intent", type="function"):
            pass  # Optional: add intent detection logic

        async with cl.Step(name="Consulting Fitness Coach", type="tool"):
            response = await self.fitness_agent.get_response(messages=message, thread=self.fitness_thread)
            agent_reply = response.message.content if hasattr(response, "message") else str(response)

        summary = agent_reply[:10] + "..." if len(agent_reply) > 10 else agent_reply
        async with cl.Step(name=f"Fitness Coach: {summary}", type="function"):
            pass

        return agent_reply

    
    @kernel_function(name="route_to_nutrition", description="Route a nutrition-related task.")
    async def route_to_nutrition(self, message: str) -> str:
        print("🥗 What manager send to nutrition_agent：", message)
        async with cl.Step(name="Analyzing user intent", type="function"):
            pass

        async with cl.Step(name="Consulting Nutrition Advisor", type="tool"):
            response = await self.nutrition_agent.get_response(messages=message, thread=self.nutrition_thread)
            agent_reply = response.message.content if hasattr(response, "message") else str(response)

        summary = agent_reply[:10] + "..." if len(agent_reply) > 10 else agent_reply
        async with cl.Step(name=f"Nutrition Advisor: {summary}", type="function"):
            pass

        return agent_reply

    @kernel_function(name="route_to_mentalcare", description="Route a mental health-related task.")
    async def route_to_mentalcare(self, message: str) -> str:
        print("🧘 What manager send to mentalcare_agent：", message)
        async with cl.Step(name="Analyzing user intent", type="function"):
            pass

        async with cl.Step(name="Consulting Mental Health Advisor", type="tool"):
            response = await self.mentalcare_agent.get_response(messages=message, thread=self.mentalcare_thread)
            agent_reply = response.message.content if hasattr(response, "message") else str(response)

        summary = agent_reply[:10] + "..." if len(agent_reply) > 10 else agent_reply
        async with cl.Step(name=f"Mental Health Advisor: {summary}", type="function"):
            pass

        return agent_reply
