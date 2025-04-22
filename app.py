import asyncio
import chainlit as cl
from semantic_kernel.agents import AzureAIAgentThread
from semantic_kernel import Kernel
from services.openai_service import get_openai_service
from agents.health_manager import create_health_manager
from agents.nutrition_agent import create_nutrition_agent
from agents.fitness_agent import create_fitness_agent
from agents.mentalcare_agent import create_mentalcare_agent
from typing import Optional
health_manager = None  # Global instance

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "123"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None

@cl.on_chat_start
async def on_chat_start():
    global health_manager

    # Auth
    user = cl.user_session.get("user")
    await cl.Message(content=f"🎉 Hello {user.identifier}, welcome to HealthManager!").send()

    kernel = Kernel()
    kernel.add_service(get_openai_service())

    # Create sub-agents and their threads
    nutrition_agent, nutrition_client, nutrition_creds = await create_nutrition_agent()
    fitness_agent, fitness_client, fitness_creds = await create_fitness_agent()
    mentalcare_agent, mentalcare_client, mentalcare_creds = await create_mentalcare_agent()

    nutrition_thread = AzureAIAgentThread(client=nutrition_client)
    fitness_thread = AzureAIAgentThread(client=fitness_client)
    mentalcare_thread = AzureAIAgentThread(client=mentalcare_client)

    # Create the health manager
    health_manager = await create_health_manager(
        kernel,
        nutrition_agent, nutrition_thread,
        fitness_agent, fitness_thread,
        mentalcare_agent, mentalcare_thread
    )

    # Save resources to session for cleanup
    cl.user_session.set("threads", [
        (nutrition_thread, nutrition_client, nutrition_creds),
        (fitness_thread, fitness_client, fitness_creds),
        (mentalcare_thread, mentalcare_client, mentalcare_creds)
    ])

    await cl.Message(content="🤖 HealthManager is ready. How can I help you today?").send()


@cl.on_message
async def on_message(message: cl.Message):
    global health_manager
    async for msg in health_manager.invoke(messages=message.content):
        await cl.Message(content=msg.message.content).send()


@cl.on_chat_end
async def on_chat_end():
    threads = cl.user_session.get("threads")
    if threads:
        for thread, client, creds in threads:
            await thread.delete()
            await client.close()
            await creds.close()
