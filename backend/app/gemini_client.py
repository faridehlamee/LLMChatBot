import google.generativeai as genai
from typing import List, Optional
from .models import ChatMessage
from .knowledge_base import KnowledgeBase
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from business_config import SYSTEM_PROMPT_TEMPLATE

class GeminiClient:
    """Client for interacting with Google Gemini AI"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-1.5-flash", knowledge_base: KnowledgeBase = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model
        self.knowledge_base = knowledge_base or KnowledgeBase()
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    async def generate_response(self, message: str, conversation_history: List[ChatMessage] = None) -> str:
        """Generate a response using Google Gemini"""
        try:
            # Check if we have a trained answer for this question
            trained_answer = self.knowledge_base.get_answer(message)
            if trained_answer:
                return trained_answer
            
            # Build the context
            context = self._build_context(message, conversation_history)
            
            # Generate response
            response = self.model.generate_content(context)
            return response.text
            
        except Exception as e:
            return f"I encountered an issue: {str(e)}. Please try again."
    
    def _build_context(self, message: str, conversation_history: List[ChatMessage] = None) -> str:
        """Build context from conversation history and knowledge base"""
        context = SYSTEM_PROMPT_TEMPLATE + "\n\n"
        
        # Add personality traits
        personality_traits = self.knowledge_base.get_personality_traits()
        if personality_traits:
            context += "PERSONALITY TRAITS:\n"
            for trait, value in personality_traits.items():
                context += f"- {trait}: {value}\n"
            context += "\n"
        
        # Add relevant facts
        facts = self.knowledge_base.get_facts()
        if facts:
            context += "IMPORTANT FACTS:\n"
            for fact in facts:
                context += f"- {fact}\n"
            context += "\n"
        
        # Add example conversations for context
        examples = self.knowledge_base.get_example_conversations()
        if examples:
            context += "EXAMPLE CONVERSATIONS:\n"
            for example in examples[-3:]:  # Use last 3 examples
                context += f"User: {example['user']}\nAssistant: {example['assistant']}\n\n"
        
        # Add conversation history if available
        if conversation_history:
            context += "CONVERSATION HISTORY:\n"
            for msg in conversation_history[-6:]:  # Last 6 messages
                role = "User" if msg.role == "user" else "Assistant"
                context += f"{role}: {msg.content}\n"
            context += "\n"
        
        context += f"Please respond to: {message}"
        return context
    
    async def check_health(self) -> bool:
        """Check if Gemini service is available"""
        try:
            # Simple test request
            test_response = self.model.generate_content("Hello")
            return test_response.text is not None
        except:
            return False
    
    async def close(self):
        """Close any resources (Gemini doesn't need explicit closing)"""
        pass
