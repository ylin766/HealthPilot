import chainlit as cl
from semantic_kernel.agents import AzureAIAgentThread
from semantic_kernel import Kernel
from services.openai_service import get_openai_service
from agents.health_manager import create_health_manager
from agents.nutrition_agent import create_nutrition_agent
from agents.fitness_agent import create_fitness_agent
from agents.mentalcare_agent import create_mentalcare_agent

# Global instance
health_manager = None  

# Auth
@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("admin", "123"):
        return cl.User(identifier="admin", metadata={"role": "admin", "provider": "credentials"})
    return None

@cl.on_chat_start
async def on_chat_start():
    global health_manager
    user = cl.user_session.get("user")

    kernel = Kernel()
    kernel.add_service(get_openai_service())

    # Create agents
    nutrition_agent, nutrition_client, nutrition_creds = await create_nutrition_agent()
    fitness_agent, fitness_client, fitness_creds = await create_fitness_agent()
    mentalcare_agent, mentalcare_client, mentalcare_creds = await create_mentalcare_agent()

    # Create threads
    nutrition_thread = AzureAIAgentThread(client=nutrition_client)
    fitness_thread = AzureAIAgentThread(client=fitness_client)
    mentalcare_thread = AzureAIAgentThread(client=mentalcare_client)

    # Health manager
    health_manager = await create_health_manager(
        kernel,
        nutrition_agent, nutrition_thread,
        fitness_agent, fitness_thread,
        mentalcare_agent, mentalcare_thread
    )

    cl.user_session.set("threads", [
        (nutrition_thread, nutrition_client, nutrition_creds),
        (fitness_thread, fitness_client, fitness_creds),
        (mentalcare_thread, mentalcare_client, mentalcare_creds)
    ])

# Chat logic
@cl.on_message
async def on_message(message: cl.Message):
    global health_manager
    async for msg in health_manager.invoke(messages=message.content):
        content = msg.message.content
        await cl.Message(content=content).send()

# Clear when end chat
@cl.on_chat_end
async def on_chat_end():
    threads = cl.user_session.get("threads")
    if threads:
        for thread, client, creds in threads:
            await thread.delete()
            await client.close()
            await creds.close()

# Prompt tutorials for users
@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="",
            message="",
            icon="/public/avatars/fitness.png",
        ),
        cl.Starter(
            label="",
            message="",
            icon="/public/avatars/fitness.png",
        )
    ]

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)