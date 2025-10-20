#!/usr/bin/env python3
"""
LLM ChatBot Server Startup Script
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

if __name__ == "__main__":
    import uvicorn
    from app.main import app
    
    print("Starting LLM ChatBot Server...")
    print("Web interface: http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/api/health")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
