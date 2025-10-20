@echo off
echo Starting LLM ChatBot Backend...
echo.

echo Checking if Ollama is running...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Ollama is not running or not accessible at http://localhost:11434
    echo Please install and start Ollama first:
    echo 1. Download from https://ollama.ai/
    echo 2. Install Ollama
    echo 3. Run: ollama pull llama2
    echo 4. Start Ollama service
    echo.
    echo The chatbot will still start but LLM features will not work.
    echo.
)

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting FastAPI server...
echo Web interface will be available at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
