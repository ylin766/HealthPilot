from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def get_openai_service():
    """
    Create an AzureChatCompletion service instance using Azure OpenAI configuration.
    All credentials are loaded from environment variables:
        - AZURE_OPENAI_API_KEY
        - AZURE_OPENAI_ENDPOINT
        - AZURE_OPENAI_DEPLOYMENT_NAME
        - AZURE_OPENAI_API_VERSION
    """
    return AzureChatCompletion(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )
