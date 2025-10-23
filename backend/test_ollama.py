#!/usr/bin/env python3
"""
Test Ollama client connection
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.llm_client import OllamaClient

async def test_ollama():
    print("Testing Ollama client...")
    
    try:
        client = OllamaClient()
        print(f"Ollama URL: {client.base_url}")
        print(f"Ollama Model: {client.model}")
        
        # Test health check
        health = await client.check_health()
        print(f"Health check: {'✅ Healthy' if health else '❌ Unhealthy'}")
        
        # Test a simple request
        if health:
            print("Testing simple request...")
            response = await client.generate_response("Hello, test message")
            print(f"Response: {response[:100]}...")
        
        await client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ollama())
