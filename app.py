import chainlit as cl
from semantic_kernel.agents import AzureAIAgentThread
from semantic_kernel import Kernel
from services.openai_service import get_openai_service
from agents.health_manager import create_health_manager
from agents.nutrition_agent import create_nutrition_agent
from agents.fitness_agent import create_fitness_agent
from agents.mentalcare_agent import create_mentalcare_agent
from semantic_kernel.contents.chat_history import ChatHistory

health_manager = None

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("admin", "123"):
        return cl.User(identifier="admin", metadata={"role": "admin", "provider": "credentials"})
    return None

@cl.on_chat_start
async def on_chat_start():
    global health_manager
    user = cl.user_session.get("user")

    cl.user_session.set("chat_history", ChatHistory())

    kernel = Kernel()
    kernel.add_service(get_openai_service())

    nutrition_agent, nutrition_client, nutrition_creds = await create_nutrition_agent()
    fitness_agent, fitness_client, fitness_creds = await create_fitness_agent()
    mentalcare_agent, mentalcare_client, mentalcare_creds = await create_mentalcare_agent()

    nutrition_thread = AzureAIAgentThread(client=nutrition_client)
    fitness_thread = AzureAIAgentThread(client=fitness_client)
    mentalcare_thread = AzureAIAgentThread(client=mentalcare_client)

    cl.user_session.set("agent_runs", {
        "nutrition": {"thread": nutrition_thread, "run_id": None},
        "fitness": {"thread": fitness_thread, "run_id": None},
        "mentalcare": {"thread": mentalcare_thread, "run_id": None}
    })

    cl.user_session.set("threads", [
        (nutrition_thread, nutrition_client, nutrition_creds),
        (fitness_thread, fitness_client, fitness_creds),
        (mentalcare_thread, mentalcare_client, mentalcare_creds)
    ])

    health_manager = await create_health_manager(
        kernel,
        nutrition_agent, nutrition_thread,
        fitness_agent, fitness_thread,
        mentalcare_agent, mentalcare_thread
    )

@cl.on_message
async def on_message(message: cl.Message):
    global health_manager

    await cancel_active_runs()

    chat_history: ChatHistory = cl.user_session.get("chat_history")

    structured_prompt = ""
    if chat_history.messages:
        structured_prompt += "<history>\n"
        for m in chat_history.messages:
            role = m.role
            content = m.content
            structured_prompt += f"{role}: {content}\n"
        structured_prompt += "</history>\n\n"

    structured_prompt += "<current>\n"
    structured_prompt += f"<message role=\"user\">{message.content}</message>\n"
    structured_prompt += "</current>"
    
    async for msg in health_manager.invoke(messages=structured_prompt):
        content = msg.message.content

        chat_history.add_user_message(message.content)
        chat_history.add_assistant_message(content)

        await cl.Message(content=content, author="HealthManager").send()

        agent_runs = cl.user_session.get("agent_runs")
        for agent_name, data in agent_runs.items():
            run_id = getattr(data["thread"], "last_run_id", None)
            if run_id:
                data["run_id"] = run_id

async def cancel_active_runs():
    agent_runs = cl.user_session.get("agent_runs")
    for data in agent_runs.values():
        thread = data["thread"]
        run_id = data.get("run_id")
        if run_id:
            try:
                await thread.cancel_run(run_id)
            except Exception:
                pass
            data["run_id"] = None

@cl.on_stop
async def on_stop():
    await cancel_active_runs()

@cl.on_chat_end
async def on_chat_end():
    await cancel_active_runs()
    threads = cl.user_session.get("threads")
    if threads:
        for thread, client, creds in threads:
            await thread.delete()
            await client.close()
            await creds.close()

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="General Health Question",
            message="I want to live a healthier life. Can you give me some general advice?",
            icon="/public/health.png",
        ),
        cl.Starter(
            label="Fitness Question",
            message="I want to strongthen my arm. Can you suggest a workout plan with 5 actions?",
            icon="/public/fitness.png",
        ),
        cl.Starter(
            label="Nutrition Question",
            message="I would like to make a meal using chicken. Could you recommend a healthy recipe?",
            icon="/public/nutrition.png",
        ),
        cl.Starter(
            label="Mental Health Question",
            message="How can I manage stress and improve my sleep quality?",
            icon="/public/mental.png",
        )
    ]
