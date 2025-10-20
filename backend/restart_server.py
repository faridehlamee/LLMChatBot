#!/usr/bin/env python3
"""
Restart the LLM ChatBot Server
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def restart_server():
    """Restart the server with the latest changes"""
    print("Restarting LLM ChatBot Server...")
    
    # Kill any existing uvicorn processes
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                         capture_output=True, text=True)
        else:  # Unix/Linux/Mac
            subprocess.run(['pkill', '-f', 'uvicorn'], 
                         capture_output=True, text=True)
    except:
        pass
    
    time.sleep(2)
    
    # Start the server
    try:
        subprocess.run([sys.executable, 'run_server.py'])
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    restart_server()
