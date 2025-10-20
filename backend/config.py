"""
Production configuration for Kiatech Software AI Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Production settings
PRODUCTION = os.getenv("PRODUCTION", "false").lower() == "true"
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

# LLM Provider selection
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # "ollama" or "gemini"

# Ollama settings (you'll need to set these in production)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

# Gemini settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Knowledge base file path
KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", "knowledge_base.json")

print(f"Starting in {'PRODUCTION' if PRODUCTION else 'DEVELOPMENT'} mode")
print(f"Host: {HOST}, Port: {PORT}")
print(f"LLM Provider: {LLM_PROVIDER}")
if LLM_PROVIDER == "ollama":
    print(f"Ollama URL: {OLLAMA_URL}")
    print(f"Ollama Model: {OLLAMA_MODEL}")
elif LLM_PROVIDER == "gemini":
    print(f"Gemini Model: {GEMINI_MODEL}")
    print(f"Gemini API Key: {'Set' if GEMINI_API_KEY else 'Not Set'}")
