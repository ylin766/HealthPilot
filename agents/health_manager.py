from semantic_kernel.agents import ChatCompletionAgent
from services.openai_service import get_openai_service
from plugins.health_manager_plugin import HealthManagerPlugin
from agents.nutrition_agent import create_nutrition_agent
from agents.fitness_agent import create_fitness_agent
from agents.mentalcare_agent import create_mentalcare_agent
from plugins.user_profile_query_plugin import UserProfileQueryPlugin
from plugins.mcp_plugin import SmtpPlugin


async def create_health_manager(
    kernel,
    nutrition_agent,
    nutrition_thread,
    fitness_agent,
    fitness_thread,
    mentalcare_agent,
    mentalcare_thread,
):
    health_manager_plugin = HealthManagerPlugin(
        nutrition_agent=nutrition_agent,
        nutrition_thread=nutrition_thread,
        fitness_agent=fitness_agent,
        fitness_thread=fitness_thread,
        mentalcare_agent=mentalcare_agent,
        mentalcare_thread=mentalcare_thread,
    )

    query_plugin = UserProfileQueryPlugin()
    smtp_plugin = SmtpPlugin()

    return ChatCompletionAgent(
        kernel=kernel,
        name="HealthManager",
        plugins=[health_manager_plugin, query_plugin, smtp_plugin],
        instructions="""You are HealthManager, an agent that routes user requests based on conversation history and current input.

You are provided with:
- Conversation history (a list of user and assistant messages)
- The user's latest message

Your tasks:
1. Carefully read the history and current user input. If user's input includes personal info, use plugin to create or update data.

2. Identify the most recent user request related to:
   - Fitness, exercise, physical training, physical health
   - Diet, nutrition, meal planning, recipes
   - Mental health, emotional wellbeing
   - Other related fields

3. Determine which agent (Fitness, Nutrition, or MentalCare) is most appropriate to handle the user's latest intent.

4. If a specific service is needed:
   - Generate a proper prompt including stored user health information
   - Delegate to the corresponding agent using the appropriate plugin

5. For email-related requests:
   - Request user's email address
   - Prepare content based on user request and agent response
   - When sending the email for body content, use html format and make it look good.
   - Use SmtpPlugin to send the email

Note: The plugin you call will NOT return anything directly. After calling the plugin, stay silent and do not answer.

If the user's request does not involve any of the areas above, answer directly yourself."""
    )
