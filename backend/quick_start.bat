@echo off
echo ========================================
echo    LLM ChatBot - Quick Start
echo ========================================
echo.

echo Starting LLM ChatBot Server...
echo.

echo IMPORTANT: Your chatbot will work in fallback mode!
echo To get full AI capabilities:
echo 1. Install Ollama from https://ollama.ai/
echo 2. Run: ollama pull llama2
echo 3. Restart this script
echo.

echo Server starting at: http://localhost:8000
echo Press Ctrl+C to stop
echo ========================================
echo.

python run_server.py

pause
