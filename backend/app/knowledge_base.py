"""
Knowledge Base for ChatBot Training
"""

import json
import os
from typing import Dict, List, Optional

class KnowledgeBase:
    """Simple knowledge base for storing and retrieving training data"""
    
    def __init__(self, file_path: str = "knowledge_base.json"):
        self.file_path = file_path
        self.knowledge = self._load_knowledge()
    
    def _load_knowledge(self) -> Dict:
        """Load knowledge base from file"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "qa_pairs": {},  # Question-Answer pairs
            "personality": {},  # Personality traits
            "examples": [],  # Example conversations
            "facts": []  # General facts about the user or topics
        }
    
    def _save_knowledge(self):
        """Save knowledge base to file"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, indent=2, ensure_ascii=False)
    
    def add_qa_pair(self, question: str, answer: str):
        """Add a question-answer pair"""
        self.knowledge["qa_pairs"][question.lower()] = answer
        self._save_knowledge()
    
    def get_answer(self, question: str) -> Optional[str]:
        """Get answer for a question"""
        return self.knowledge["qa_pairs"].get(question.lower())
    
    def add_personality_trait(self, trait: str, value: str):
        """Add personality trait"""
        self.knowledge["personality"][trait] = value
        self._save_knowledge()
    
    def get_personality_traits(self) -> Dict:
        """Get all personality traits"""
        return self.knowledge["personality"]
    
    def add_fact(self, fact: str):
        """Add a fact to the knowledge base"""
        if fact not in self.knowledge["facts"]:
            self.knowledge["facts"].append(fact)
            self._save_knowledge()
    
    def get_facts(self) -> List:
        """Get all facts"""
        return self.knowledge["facts"]
    
    def add_example_conversation(self, user_message: str, assistant_response: str):
        """Add example conversation"""
        self.knowledge["examples"].append({
            "user": user_message,
            "assistant": assistant_response
        })
        self._save_knowledge()
    
    def get_example_conversations(self) -> List:
        """Get all example conversations"""
        return self.knowledge["examples"]
    
    def get_context(self) -> str:
        """Get knowledge context for the AI"""
        context = ""
        
        if self.knowledge["personality"]:
            context += "Personality traits:\n"
            for trait, value in self.knowledge["personality"].items():
                context += f"- {trait}: {value}\n"
            context += "\n"
        
        if self.knowledge["facts"]:
            context += "Known facts:\n"
            for fact in self.knowledge["facts"][-5:]:  # Last 5 facts
                context += f"- {fact}\n"
            context += "\n"
        
        return context
    
    def search_qa(self, query: str) -> Optional[str]:
        """Search for similar questions and return answers"""
        query_lower = query.lower()
        
        # Exact match
        if query_lower in self.knowledge["qa_pairs"]:
            return self.knowledge["qa_pairs"][query_lower]
        
        # Partial match
        for question, answer in self.knowledge["qa_pairs"].items():
            if any(word in question for word in query_lower.split()):
                return answer
        
        return None
