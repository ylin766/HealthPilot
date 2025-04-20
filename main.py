import asyncio
from semantic_kernel.agents import AzureAIAgentThread
from semantic_kernel import Kernel
from services.openai_service import get_openai_service
from agents.health_manager import create_health_manager
from agents.nutrition_agent import create_nutrition_agent
from agents.fitness_agent import create_fitness_agent
from agents.mentalcare_agent import create_mentalcare_agent

async def main():
    kernel = Kernel()
    kernel.add_service(get_openai_service())
    # create Nutrition Agent
    nutrition_agent, nutrition_client, nutrition_creds = await create_nutrition_agent()
    nutrition_thread = AzureAIAgentThread(client=nutrition_client)

    # create Fitness Agent
    fitness_agent, fitness_client, fitness_creds = await create_fitness_agent()
    fitness_thread = AzureAIAgentThread(client=fitness_client)

    # create MentalCare Agent
    mentalcare_agent, mentalcare_client, mentalcare_creds = await create_mentalcare_agent()
    mentalcare_thread = AzureAIAgentThread(client=mentalcare_client)

    # creat HealthManager & input all Agent
    health_manager = await create_health_manager(
        kernel,
        nutrition_agent, nutrition_thread,
        fitness_agent, fitness_thread,
        mentalcare_agent, mentalcare_thread
    )

    print("🤖 HealthManager is online. Type 'exit' to quit.\n")

    try:
        while True:
            user_input = input("🧑‍💻 You: ").strip()
            if user_input.lower() in {"exit", "quit"}:
                break

            async for msg in health_manager.invoke(messages=user_input):
                print(msg.message.content)
    finally:
        # clear 
        await nutrition_thread.delete()
        await nutrition_client.close()
        await nutrition_creds.close()

        await fitness_thread.delete()
        await fitness_client.close()
        await fitness_creds.close()

        await mentalcare_thread.delete()
        await mentalcare_client.close()
        await mentalcare_creds.close()

if __name__ == "__main__":
    asyncio.run(main())