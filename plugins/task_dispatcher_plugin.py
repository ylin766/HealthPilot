from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread

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
        response = await self.fitness_agent.get_response(messages=message, thread=self.fitness_thread)
        return f"{response}"

    @kernel_function(name="route_to_nutrition", description="Route a nutrition-related task.")
    async def route_to_nutrition(self, message: str) -> str:
        print("🥗 What manager send to nutrition_agent：", message)
        response = await self.nutrition_agent.get_response(messages=message, thread=self.nutrition_thread)
        return f"{response}"

    @kernel_function(name="route_to_mentalcare", description="Route a mental health-related task.")
    async def route_to_mentalcare(self, message: str) -> str:
        print("🧘 What manager send to mentalcare_agent：", message)
        response = await self.mentalcare_agent.get_response(messages=message, thread=self.mentalcare_thread)
        return f"{response}"
