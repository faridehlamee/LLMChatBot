from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    """Represents a single chat message"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    """Request model for chat API"""
    message: str
    conversation_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    """Response model for chat API"""
    response: str
    conversation_history: List[ChatMessage]
    model_used: str
    processing_time: float

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    llm_status: str
