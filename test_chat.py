import requests
import json

# Test the chat API
url = "http://127.0.0.1:8000/api/chat"
data = {
    "message": "What services do you offer?"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
