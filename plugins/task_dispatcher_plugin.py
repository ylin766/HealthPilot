from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread
import chainlit as cl
import json
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
        async with cl.Step(name="Consulting Fitness Coach", type="tool"):
            response = await self.fitness_agent.get_response(messages=message, thread=self.fitness_thread)
            agent_reply = response.message.content if hasattr(response, "message") else str(response)
        
        content = agent_reply
        
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
                        elements=[
                            cl.CustomElement(
                                name="VideoPlayer",
                                props=props,
                                display="inline"
                            )
                        ],
                        author="Fitness Agent"
                    ).send()

                elif item_type == "text_block":
                    await cl.Message(
                        content="",
                        elements=[
                            cl.CustomElement(
                                name="TextPlayer",
                                props={
                                    "title": title,
                                    "content": props.get("content", "")
                                },
                                display="inline"
                            )
                        ],
                        author="Fitness Agent"
                    ).send()

                else:
                    await cl.Message(
                        content=f"📦 Unsupported render block: {item_type}",
                        author="Fitness Agent"
                    ).send()

        except Exception:
            await cl.Message(content=content, author="Fitness Agent").send()

    @kernel_function(name="route_to_nutrition", description="Route a nutrition-related task.")
    async def route_to_nutrition(self, message: str) -> str:
        async with cl.Step(name="Consulting Nutrition Advisor", type="tool"):
            response = await self.nutrition_agent.get_response(messages=message, thread=self.nutrition_thread)
            agent_reply = response.message.content if hasattr(response, "message") else str(response)

        content = agent_reply
        
        try:
            parsed = json.loads(content)
            render_items = parsed.get("render", [])
            if not render_items:
                raise ValueError("No render items")

            for item in render_items:
                if item["type"] == "text_block":
                    await cl.Message(content="", elements=[
                        cl.CustomElement(
                            name="TextPlayer",
                            props={
                                "title": item["title"],
                                "content": item["props"]["content"]
                            }
                        )], author="Nutrition Agent"
                    ).send()
                elif item["type"] == "image_note_block":
                    await cl.Message(content="", elements=[
                        cl.CustomElement(
                            name="ImagePlayer",
                            props={
                                "title": item["title"],
                                "imageUrl": item["props"]["imageUrl"],
                                "note": item["props"].get("note", "")
                            }
                        )], author="Nutrition Agent"
                    ).send()
                    
                else:
                    await cl.Message(content=f"📦 Unsupported render block: {item}", author="Nutrition Agent").send()


        except Exception as e:
            await cl.Message(content=content, author="Nutrition Agent").send()


    @kernel_function(name="route_to_mentalcare", description="Route a mental health-related task.")
    async def route_to_mentalcare(self, message: str) -> str:
        async with cl.Step(name="Consulting Mental Health Advisor", type="tool"):
            response = await self.mentalcare_agent.get_response(messages=message, thread=self.mentalcare_thread)
            agent_reply = response.message.content if hasattr(response, "message") else str(response)

            
