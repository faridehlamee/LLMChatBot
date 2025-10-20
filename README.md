# LLM ChatBot Project

A complete AI chatbot solution with local LLM support and Android app integration.

## Project Structure

```
LLMChatBot/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI application
│   │   ├── chatbot.py     # Chatbot logic
│   │   ├── llm_client.py  # Local LLM integration
│   │   └── models.py      # Pydantic models
│   ├── static/            # Static files for web UI
│   ├── templates/         # HTML templates
│   └── requirements.txt
├── android/               # Android app (to be created)
├── docs/                  # Documentation
└── README.md
```

## Features

- 🤖 AI-powered chatbot with local LLM support
- 🌐 REST API for Android app integration
- 💻 Web interface for testing
- 📱 Android app (planned)
- 🔒 Privacy-focused (runs locally)

## Setup Instructions

### 1. Install Local LLM (Ollama)

Download and install Ollama from: https://ollama.ai/

```bash
# Install a model (e.g., Llama 2)
ollama pull llama2
```

### 2. Setup Python Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 3. Access the Application

- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Endpoints

- `POST /api/chat` - Send message to chatbot
- `GET /api/health` - Health check
- `GET /` - Web interface

## Android App Integration

The Android app will communicate with the backend via REST API calls to `/api/chat` endpoint.

## Development Status

- [x] Project structure
- [x] Backend API
- [x] Local LLM integration
- [x] Web interface
- [ ] Android app development
- [ ] Testing and optimization
