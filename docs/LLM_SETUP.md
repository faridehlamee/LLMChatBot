# Local LLM Setup Guide

This guide will help you set up a local Large Language Model (LLM) to power your chatbot.

## Option 1: Ollama (Recommended)

Ollama is the easiest way to run LLMs locally on your PC.

### Installation

1. **Download Ollama**
   - Visit [https://ollama.ai/](https://ollama.ai/)
   - Download the installer for Windows
   - Run the installer and follow the setup wizard

2. **Install a Model**
   ```bash
   # Install Llama 2 (7B parameters, ~4GB)
   ollama pull llama2
   
   # Or install a smaller model for testing
   ollama pull llama2:7b-chat
   
   # For better performance (if you have more RAM)
   ollama pull llama2:13b-chat
   ```

3. **Start Ollama Service**
   - Ollama should start automatically after installation
   - You can verify it's running by visiting: http://localhost:11434

### Available Models

| Model | Size | RAM Required | Description |
|-------|------|--------------|-------------|
| llama2:7b-chat | ~4GB | 8GB+ | Good balance of performance and resource usage |
| llama2:13b-chat | ~7GB | 16GB+ | Better quality responses |
| llama2:70b-chat | ~40GB | 64GB+ | Best quality (requires powerful hardware) |
| codellama:7b | ~4GB | 8GB+ | Specialized for coding tasks |
| mistral:7b | ~4GB | 8GB+ | Fast and efficient alternative |

## Option 2: LM Studio

LM Studio provides a GUI for managing local LLMs.

1. **Download LM Studio**
   - Visit [https://lmstudio.ai/](https://lmstudio.ai/)
   - Download and install

2. **Download a Model**
   - Open LM Studio
   - Go to the "Models" tab
   - Search for and download a model (e.g., "Llama 2 7B Chat")

3. **Start Local Server**
   - Go to the "Local Server" tab
   - Click "Start Server"
   - Note the API endpoint (usually http://localhost:1234)

## Option 3: Hugging Face Transformers

For advanced users who want more control:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load model
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Use in your application
```

## Configuration

Update the chatbot configuration in `backend/app/llm_client.py`:

```python
# For Ollama (default)
self.base_url = "http://localhost:11434"
self.model = "llama2"

# For LM Studio
self.base_url = "http://localhost:1234"
self.model = "your-model-name"

# For custom API
self.base_url = "http://your-custom-endpoint"
self.model = "your-model"
```

## Performance Tips

1. **RAM Requirements**
   - 7B models: 8GB+ RAM recommended
   - 13B models: 16GB+ RAM recommended
   - 70B models: 64GB+ RAM recommended

2. **GPU Acceleration**
   - Install CUDA for NVIDIA GPUs
   - Install ROCm for AMD GPUs
   - Ollama will automatically use GPU if available

3. **Model Selection**
   - Start with smaller models for testing
   - Upgrade to larger models for better quality
   - Consider specialized models for specific tasks

## Troubleshooting

### Ollama Not Starting
```bash
# Check if Ollama is running
ollama list

# Restart Ollama service
ollama serve
```

### Out of Memory Errors
- Use smaller models
- Close other applications
- Increase virtual memory

### Slow Responses
- Use GPU acceleration
- Reduce model size
- Optimize conversation history length

## Testing Your Setup

1. Start your chatbot backend
2. Visit http://localhost:8000
3. Check the status indicator (should show "LLM Online")
4. Send a test message

If the status shows "LLM Offline", check:
- Ollama is running
- Model is downloaded (`ollama list`)
- No firewall blocking port 11434
