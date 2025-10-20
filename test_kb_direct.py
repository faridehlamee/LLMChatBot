import httpx
import asyncio
import json

async def test_knowledge_base_direct():
    """Test the knowledge base directly"""
    url = "http://127.0.0.1:8000/api/train/knowledge"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            knowledge = response.json()
            
            print("Knowledge Base Contents:")
            print(json.dumps(knowledge, indent=2))
            
            # Test the specific question
            question = "do you offer maintenance?"
            qa_pairs = knowledge.get("qa_pairs", {})
            
            print(f"\nLooking for question: '{question}'")
            print(f"Available questions: {list(qa_pairs.keys())}")
            
            if question in qa_pairs:
                print(f"Found answer: {qa_pairs[question]}")
            else:
                print("Question not found in knowledge base!")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_knowledge_base_direct())
