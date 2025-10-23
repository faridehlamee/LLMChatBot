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
    """Main chatbot service that handles conversation logic with intelligent fallback"""
    
    def __init__(self, knowledge_base=None):
        self.knowledge_base = knowledge_base
        self.conversation_history: List[ChatMessage] = []
        
        # Initialize both clients for fallback capability
        self.gemini_client = None
        self.ollama_client = None
        
        # Try to initialize Gemini if API key is available
        if GEMINI_API_KEY and GEMINI_API_KEY.strip():
            try:
                self.gemini_client = GeminiClient(
                    api_key=GEMINI_API_KEY,
                    model=GEMINI_MODEL,
                    knowledge_base=knowledge_base
                )
            except Exception as e:
                print(f"Failed to initialize Gemini client: {e}")
        
        # Always initialize Ollama client as fallback
        try:
            self.ollama_client = OllamaClient(
                base_url=OLLAMA_URL,
                model=OLLAMA_MODEL,
                knowledge_base=knowledge_base
            )
        except Exception as e:
            print(f"Failed to initialize Ollama client: {e}")
        
        # Determine primary client based on configuration
        if LLM_PROVIDER == "gemini" and self.gemini_client:
            self.primary_client = self.gemini_client
            self.fallback_client = self.ollama_client
        else:
            self.primary_client = self.ollama_client
            self.fallback_client = self.gemini_client
    
    async def process_message(self, request: ChatRequest) -> ChatResponse:
        """Process a user message and return chatbot response with intelligent fallback"""
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
        
        # Try primary client first, then fallback if needed
        response_text = await self._generate_response_with_fallback(
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
            model_used=getattr(self.primary_client, 'model_name', getattr(self.primary_client, 'model', 'unknown')),
            processing_time=processing_time
        )
    
    async def _generate_response_with_fallback(self, message: str, conversation_history: List[ChatMessage]) -> str:
        """Generate response with automatic fallback on quota/error"""
        # Try primary client first
        if self.primary_client:
            try:
                response = await self.primary_client.generate_response(message, conversation_history)
                
                # Check if response indicates quota exceeded
                if "quota" in response.lower() and "exceeded" in response.lower():
                    print("Primary client quota exceeded, trying fallback...")
                    if self.fallback_client:
                        return await self.fallback_client.generate_response(message, conversation_history)
                    else:
                        return "I'm currently experiencing high demand. Please try again later or contact support."
                
                return response
                
            except Exception as e:
                print(f"Primary client error: {e}, trying fallback...")
                if self.fallback_client:
                    try:
                        return await self.fallback_client.generate_response(message, conversation_history)
                    except Exception as fallback_error:
                        print(f"Fallback client also failed: {fallback_error}")
                        return f"I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"
                else:
                    return f"I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"
        
        # If no primary client, try fallback
        elif self.fallback_client:
            try:
                return await self.fallback_client.generate_response(message, conversation_history)
            except Exception as e:
                return f"I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"
        
        return "No LLM services are currently available. Please check your configuration."
    
    async def check_llm_health(self) -> bool:
        """Check if any LLM service is available"""
        if self.primary_client:
            try:
                if await self.primary_client.check_health():
                    return True
            except:
                pass
        
        if self.fallback_client:
            try:
                return await self.fallback_client.check_health()
            except:
                pass
        
        return False
    
    def get_conversation_history(self) -> List[ChatMessage]:
        """Get current conversation history"""
        return self.conversation_history
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []