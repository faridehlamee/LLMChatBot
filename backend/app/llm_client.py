import httpx
import json
from typing import List, Optional
from .models import ChatMessage
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from business_config import SYSTEM_PROMPT_TEMPLATE
from .knowledge_base import KnowledgeBase

class OllamaClient:
    """Client for interacting with Ollama local LLM"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1", knowledge_base: KnowledgeBase = None):
        self.base_url = base_url
        self.model = model
        self.client = httpx.AsyncClient(timeout=300.0)  # Increased timeout to 5 minutes
        self.knowledge_base = knowledge_base or KnowledgeBase()
    
    async def generate_response(self, message: str, conversation_history: List[ChatMessage] = None) -> str:
        """Generate a response using the local LLM"""
        try:
            # Check if we have a trained answer for this question
            trained_answer = self.knowledge_base.get_answer(message)
            if trained_answer:
                return trained_answer
            
            # Prepare the conversation context
            context = self._build_context(message, conversation_history)
            
            # Make request to Ollama
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": context,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "I'm sorry, I couldn't generate a response.")
            else:
                return f"Error: LLM service returned status {response.status_code}"
                
        except httpx.TimeoutException:
            return "I'm taking a bit longer to respond. Please try again in a moment - Ollama might be processing your request."
        except httpx.ConnectError:
            return "I can't connect to Ollama right now. Please make sure Ollama is running and try again."
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
        
        context += f"Please respond to: {message}"
        return context
    
    async def check_health(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
