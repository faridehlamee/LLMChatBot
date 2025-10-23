#!/usr/bin/env python3
"""
Script to start Ollama and pull the required model
"""
import subprocess
import sys
import time
import requests
import os

def check_ollama_running():
    """Check if Ollama is already running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_ollama():
    """Start Ollama service"""
    print("Starting Ollama...")
    try:
        # Try to start Ollama (this works on Windows with Ollama installed)
        subprocess.Popen(["ollama", "serve"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Wait for Ollama to start
        for i in range(30):  # Wait up to 30 seconds
            if check_ollama_running():
                print("✅ Ollama is now running!")
                return True
            time.sleep(1)
            print(f"Waiting for Ollama to start... ({i+1}/30)")
        
        print("❌ Ollama failed to start within 30 seconds")
        return False
        
    except FileNotFoundError:
        print("❌ Ollama is not installed or not in PATH")
        print("Please install Ollama from: https://ollama.ai/download")
        return False
    except Exception as e:
        print(f"❌ Error starting Ollama: {e}")
        return False

def pull_model(model_name="llama3.1"):
    """Pull the required model"""
    print(f"Pulling model: {model_name}")
    try:
        result = subprocess.run(["ollama", "pull", model_name], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ Model {model_name} pulled successfully!")
            return True
        else:
            print(f"❌ Failed to pull model: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Model pull timed out (5 minutes)")
        return False
    except Exception as e:
        print(f"❌ Error pulling model: {e}")
        return False

def main():
    print("🚀 Ollama Setup Script")
    print("=" * 50)
    
    # Check if Ollama is already running
    if check_ollama_running():
        print("✅ Ollama is already running!")
    else:
        if not start_ollama():
            sys.exit(1)
    
    # Check if model is available
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            
            if "llama3.1:latest" in model_names:
                print("✅ llama3.1 model is already available!")
            else:
                print("📥 Model not found, pulling llama3.1...")
                if not pull_model("llama3.1"):
                    print("❌ Failed to pull model. You can try manually:")
                    print("   ollama pull llama3.1")
                    sys.exit(1)
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        sys.exit(1)
    
    print("\n🎉 Setup complete! Your chatbot should now work with Ollama.")
    print("💡 Tip: Set LLM_PROVIDER=ollama in your config.env file")

if __name__ == "__main__":
    main()
