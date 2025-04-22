# 🩺 HealthPilot

**HealthPilot** is a multi-agent health management system built with Semantic Kernel and Azure OpenAI. It supports automatic task routing for nutrition, fitness, and mental health guidance.

## 📁 Project Structure

HealthPilot/
├── agents/            # Agent definitions
├── services/          # Azure/OpenAI service configs
├── app.py             # Chainlit entry point
├── .env               # Environment secrets
├── main.py            # Entry point for local test
└── requirements.txt   # Python dependencies


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

# Generate this using: chainlit create-secret
CHAINLIT_AUTH_SECRET=your_generated_secret
```

Run the project:

```bash
chainlit run app.py
```

### 🔐 Login

- Username: `admin`  
- Password: `123`

## ✅ TODO

- [ ] Frontend integration  
- [ ] Persistent user health profile  
- [Akhil] Local RAG (Retrieval-Augmented Generation)  
- [Akhil] Web search tool integration  
