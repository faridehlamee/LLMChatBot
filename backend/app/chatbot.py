from datetime import datetime
from typing import List
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .models import ChatMessage, ChatRequest, ChatResponse
from .llm_client import OllamaClient
from .gemini_client import GeminiClient
from config import LLM_PROVIDER, GEMINI_API_KEY, GEMINI_MODEL, OLLAMA_URL, OLLAMA_MODEL

class ChatbotService:
    """Main chatbot service that handles conversation logic"""
    
    def __init__(self, knowledge_base=None):
        # Initialize the appropriate LLM client based on configuration
        if LLM_PROVIDER == "gemini":
            self.llm_client = GeminiClient(
                api_key=GEMINI_API_KEY,
                model=GEMINI_MODEL,
                knowledge_base=knowledge_base
            )
        else:
            self.llm_client = OllamaClient(
                base_url=OLLAMA_URL,
                model=OLLAMA_MODEL,
                knowledge_base=knowledge_base
            )
        self.conversation_history: List[ChatMessage] = []
    
    async def process_message(self, request: ChatRequest) -> ChatResponse:
        """Process a user message and return chatbot response"""
        start_time = time.time()
        
        # Add user message to history
        user_message = ChatMessage(
            role="user",
            content=request.message,
            timestamp=datetime.now()
        )
        
        # Add any provided conversation history
        if request.conversation_history:
            self.conversation_history = request.conversation_history
        
        self.conversation_history.append(user_message)
        
        # Generate response using LLM
        response_text = await self.llm_client.generate_response(
            request.message, 
            self.conversation_history
        )
        
        # Add assistant response to history
        assistant_message = ChatMessage(
            role="assistant",
            content=response_text,
            timestamp=datetime.now()
        )
        self.conversation_history.append(assistant_message)
        
        processing_time = time.time() - start_time
        
        return ChatResponse(
            response=response_text,
            conversation_history=self.conversation_history,
            model_used=getattr(self.llm_client, 'model_name', getattr(self.llm_client, 'model', 'unknown')),
            processing_time=processing_time
        )
    
    async def check_llm_health(self) -> bool:
        """Check if the LLM service is available"""
        return await self.llm_client.check_health()
    
    def get_conversation_history(self) -> List[ChatMessage]:
        """Get current conversation history"""
        return self.conversation_history
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []