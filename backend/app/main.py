from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os

from .models import ChatRequest, ChatResponse, HealthResponse
from .chatbot import ChatbotService
from .knowledge_base import KnowledgeBase

# Initialize FastAPI app
app = FastAPI(
    title="LLM ChatBot API",
    description="AI Chatbot with local LLM support",
    version="1.0.0"
)

# Initialize shared knowledge base and chatbot service
knowledge_base = KnowledgeBase()
chatbot_service = ChatbotService(knowledge_base=knowledge_base)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main chat interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/train", response_class=HTMLResponse)
async def train_interface(request: Request):
    """Serve the training interface"""
    return templates.TemplateResponse("train.html", {"request": request})

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint for processing messages"""
    try:
        response = await chatbot_service.process_message(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    llm_status = "healthy" if await chatbot_service.check_llm_health() else "unhealthy"
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        llm_status=llm_status
    )

@app.get("/api/conversation")
async def get_conversation():
    """Get current conversation history"""
    return {"conversation": chatbot_service.get_conversation_history()}

@app.post("/api/conversation/clear")
async def clear_conversation():
    """Clear conversation history"""
    chatbot_service.clear_conversation()
    return {"message": "Conversation cleared successfully"}

# Training Endpoints
@app.post("/api/train/qa")
async def train_qa_pair(request: dict):
    """Add a question-answer pair to the knowledge base"""
    question = request.get("question")
    answer = request.get("answer")
    if not question or not answer:
        raise HTTPException(status_code=400, detail="Both question and answer are required")
    knowledge_base.add_qa_pair(question, answer)
    return {"message": f"Added QA pair: {question} -> {answer}"}

@app.post("/api/train/personality")
async def train_personality(request: dict):
    """Add personality trait"""
    trait = request.get("trait")
    value = request.get("traitValue")
    if not trait or not value:
        raise HTTPException(status_code=400, detail="Both trait and value are required")
    knowledge_base.add_personality_trait(trait, value)
    return {"message": f"Added personality trait: {trait} = {value}"}

@app.post("/api/train/fact")
async def train_fact(request: dict):
    """Add a fact to the knowledge base"""
    fact = request.get("fact")
    if not fact:
        raise HTTPException(status_code=400, detail="Fact is required")
    knowledge_base.add_fact(fact)
    return {"message": f"Added fact: {fact}"}

@app.post("/api/train/example")
async def train_example(request: dict):
    """Add example conversation"""
    user_message = request.get("userMsg")
    assistant_response = request.get("assistantMsg")
    if not user_message or not assistant_response:
        raise HTTPException(status_code=400, detail="Both user message and assistant response are required")
    knowledge_base.add_example_conversation(user_message, assistant_response)
    return {"message": "Added example conversation"}

@app.get("/api/train/knowledge")
async def get_knowledge():
    """Get all training data"""
    return knowledge_base.knowledge

@app.post("/api/train/clear")
async def clear_training_data():
    """Clear all training data"""
    knowledge_base.knowledge = {
        "qa_pairs": {},
        "personality": {},
        "examples": [],
        "facts": []
    }
    knowledge_base._save_knowledge()
    return {"message": "Training data cleared successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
