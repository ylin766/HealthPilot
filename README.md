# HealthPilot Setup Guide

## 1. Create Azure Account and Configure Agents

- Register an Azure account.
- Access **Azure AI Foundry** and create a new project.
- Create three agents using the **GPT-4o** model:
  - Fitness Agent
  - Nutrition Agent
  - MentalCare Agent
- Refer to the prompts and comments in:
  - `agents/fitness_agent.py`
  - `agents/nutrition_agent.py`
  - `agents/mentalcare_agent.py`
- Fill in the prompts based on the instructions in the files.

## 2. Deploy GPT-4o-mini Model and Configure Environment

- Deploy the **GPT-4o-mini** model in Azure.
- Create a `.env` file in the project root directory with the following content:

  ```env
  AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
  AZURE_OPENAI_API_KEY=your_api_key_here
  AZURE_OPENAI_ENDPOINT=https://your-endpoint-here.openai.azure.com/
  AZURE_OPENAI_API_VERSION="2024-12-01-preview"
  AZURE_AI_AGENT_PROJECT_CONNECTION_STRING=your_agent_project_connection_string_here
  ```

## 3. Set up Chainlit Authentication

- Generate your Chainlit secret:

  ```bash
  chainlit create-secret
  ```

- Copy the generated secret and add it to your `.env` file:

  ```env
  CHAINLIT_AUTH_SECRET=your_generated_secret_here
  ```

## 4. Install Required Packages

- Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

## 5. Launch the Application

- Run the app:

  ```bash
  chainlit run app.py
  ```
