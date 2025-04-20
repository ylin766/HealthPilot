# 🩺 HealthPilot

**HealthPilot** is a multi-agent health management system built with Semantic Kernel and Azure OpenAI. It supports automatic task routing for nutrition, fitness, and mental health guidance.

## 📁 Project Structure

HealthPilot/
├── agents/                    # Sub-agents: fitness, nutrition, mentalcare, manager  
├── plugins/                   # Task dispatcher plugin  
├── services/                  # External service configs (e.g., OpenAI)  
├── main.py                    # Entry point  
├── requirements.txt           # Python dependencies  
└── .env                       # Environment variables  

## 🚀 Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file with your Azure OpenAI settings:

```env
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=...
AZURE_OPENAI_API_VERSION=...
```

Run the project:

```bash
python main.py
```

## ✅ TODO

- [ ] Frontend integration  
- [ ] Persistent user health profile  
- [Akhil] Local RAG (Retrieval-Augmented Generation)  
- [Akhil] Web search tool integration  
