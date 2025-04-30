from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread
import chainlit as cl
import json
import sqlite3, os


class HealthManagerPlugin:
    def __init__(
        self,
        nutrition_agent: AzureAIAgent, nutrition_thread: AzureAIAgentThread,
        fitness_agent: AzureAIAgent, fitness_thread: AzureAIAgentThread,
        mentalcare_agent: AzureAIAgent, mentalcare_thread: AzureAIAgentThread,
    ):
        self.agents = {
            "fitness": (fitness_agent, fitness_thread),
            "nutrition": (nutrition_agent, nutrition_thread),
            "mentalcare": (mentalcare_agent, mentalcare_thread),
        }
        self.db_path = "data/memory.db"

    async def route_to_agent(self, agent_key: str, message: str):
        agent, thread = self.agents[agent_key]
        agent_name = agent_key.capitalize() + " Agent"

        async with cl.Step(name=f"Consulting {agent_name}", type="tool"):
            response = await agent.get_response(messages=message, thread=thread)
            content = response.message.content if hasattr(response, "message") else str(response)

        await self.render_blocks(content, agent_name)

    async def render_blocks(self, content: str, agent_name: str):
        try:
            parsed = json.loads(content)
            render_items = parsed.get("render", [])
            if not render_items:
                raise ValueError("No render items")

            for item in render_items:
                item_type = item.get("type")
                title = item.get("title", "Untitled")
                props = item.get("props", {})

                if item_type == "video_block":
                    await cl.Message(
                        content="",
                        elements=[cl.CustomElement(name="VideoPlayer", props=props, display="inline")],
                        author=agent_name
                    ).send()

                elif item_type == "text_block":
                    await cl.Message(
                        content="",
                        elements=[cl.CustomElement(name="TextPlayer", props={"title": title, "content": props.get("content", "")}, display="inline")],
                        author=agent_name
                    ).send()

                elif item_type == "image_note_block":
                    await cl.Message(
                        content="",
                        elements=[cl.CustomElement(name="ImagePlayer", props={
                            "title": title,
                            "imageUrl": props.get("imageUrl", ""),
                            "note": props.get("note", "")
                        })],
                        author=agent_name
                    ).send()

                else:
                    await cl.Message(content=f"📦 Unsupported render block: {item_type}", author=agent_name).send()

        except Exception:
            await cl.Message(content=content, author=agent_name).send()

    @kernel_function(name="route_to_fitness", description="Route a fitness-related task.")
    async def route_to_fitness(self, message: str) -> str:
        await self.route_to_agent("fitness", message)

    @kernel_function(name="route_to_nutrition", description="Route a nutrition-related task.")
    async def route_to_nutrition(self, message: str) -> str:
        await self.route_to_agent("nutrition", message)

    @kernel_function(name="route_to_mentalcare", description="Route a mental health-related task.")
    async def route_to_mentalcare(self, message: str) -> str:
        await self.route_to_agent("mentalcare", message)

    @kernel_function(name="create_user_profile", description="Create a new user profile if one does not exist.")
    async def create_user_profile(
        self,
        name: str,
        age: int,
        gender: str,
        height_cm: float,
        weight_kg: float
    ) -> str:
        user_id = cl.user_session.get("user").identifier
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                age INTEGER,
                gender TEXT,
                height_cm REAL,
                weight_kg REAL
            )
        """)

        cursor.execute("SELECT user_id FROM user_profile WHERE user_id = ?", (user_id,))
        if cursor.fetchone():
            conn.close()
            return "⚠️ Profile already exists. Use upsert to update it."

        cursor.execute("""
            INSERT INTO user_profile (user_id, name, age, gender, height_cm, weight_kg)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, name, age, gender, height_cm, weight_kg))
        conn.commit()
        conn.close()
        return "✅ New profile created."

    @kernel_function(name="upsert_user_profile", description="Update or insert user profile for the current user.")
    async def upsert_user_profile(
        self,
        name: str,
        age: int,
        gender: str,
        height_cm: float,
        weight_kg: float
    ) -> str:
        user_id = cl.user_session.get("user").identifier
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO user_profile (user_id, name, age, gender, height_cm, weight_kg)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                name=excluded.name,
                age=excluded.age,
                gender=excluded.gender,
                height_cm=excluded.height_cm,
                weight_kg=excluded.weight_kg
        """, (user_id, name, age, gender, height_cm, weight_kg))
        conn.commit()
        conn.close()
        return "✅ Profile saved (inserted or updated)."

    @kernel_function(name="delete_user_profile", description="Delete the current user's profile.")
    async def delete_user_profile(self) -> str:
        user_id = cl.user_session.get("user").identifier
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_profile WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return "🗑️ Profile deleted (if it existed)."
