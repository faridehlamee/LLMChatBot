# 🚀 Deployment Guide for Kiatech Software AI Assistant

## 📋 Prerequisites

Before deploying, you need to decide how to handle the **Ollama LLM service** in production:

### Option A: Use a Hosted LLM Service (Recommended)
- **OpenAI API**: Replace Ollama with OpenAI GPT models
- **Anthropic Claude**: Use Claude API
- **Google Gemini**: Use Google's AI API
- **Hugging Face**: Use their hosted models

### Option B: Self-host Ollama
- Deploy Ollama on a separate server
- Use services like RunPod, Replicate, or your own VPS

## 🌐 Deployment Options

### 1. Railway (Easiest - Recommended)

**Steps:**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Connect your GitHub repository
5. Railway will automatically detect it's a Python app
6. Set environment variables in Railway dashboard:
   ```
   PRODUCTION=true
   OLLAMA_URL=https://your-ollama-service.com
   OLLAMA_MODEL=llama3.1
   ```
7. Deploy!

**Pros:** Free tier, automatic deployments, easy setup
**Cons:** Limited free tier resources

### 2. Render

**Steps:**
1. Go to [render.com](https://render.com)
2. Sign up and create a new "Web Service"
3. Connect your GitHub repository
4. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables
6. Deploy!

**Pros:** Free tier, good for Python apps
**Cons:** Cold starts can be slow

### 3. Heroku

**Steps:**
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

**Pros:** Mature platform, good documentation
**Cons:** No longer has free tier

### 4. DigitalOcean App Platform

**Steps:**
1. Go to DigitalOcean App Platform
2. Create new app from GitHub
3. Configure build and run commands
4. Set environment variables
5. Deploy!

**Pros:** Good performance, reasonable pricing
**Cons:** No free tier

## 🔧 Production Configuration

### Update your LLM Client for Production

You'll need to modify `backend/app/llm_client.py` to support different LLM providers:

```python
# Add this to support multiple LLM providers
class LLMClient:
    def __init__(self, provider="ollama"):
        self.provider = provider
        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif provider == "ollama":
            self.client = httpx.AsyncClient()
        # Add more providers as needed
```

### Environment Variables to Set

```bash
# Required
PRODUCTION=true
PORT=8000

# LLM Configuration
OLLAMA_URL=https://your-ollama-service.com
OLLAMA_MODEL=llama3.1

# Or for OpenAI
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-3.5-turbo

# Optional
KNOWLEDGE_BASE_PATH=knowledge_base.json
```

## 🎯 Quick Start with Railway

1. **Prepare your code:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy to Railway:**
   - Go to railway.app
   - Connect GitHub repo
   - Railway auto-detects Python
   - Add environment variables
   - Deploy!

3. **Your chatbot will be live at:**
   `https://your-app-name.railway.app`

## 🔍 Testing Your Deployment

After deployment, test these endpoints:
- `https://your-app.com/` - Main chat interface
- `https://your-app.com/train` - Training interface
- `https://your-app.com/api/health` - Health check
- `https://your-app.com/docs` - API documentation

## 🚨 Important Notes

1. **Ollama Service**: You need a hosted Ollama service or switch to a cloud LLM API
2. **Knowledge Base**: The `knowledge_base.json` file will be reset on each deployment
3. **Static Files**: Make sure your templates and static files are included
4. **Environment Variables**: Set all required environment variables in your deployment platform

## 💡 Next Steps

1. Choose a deployment platform
2. Set up a hosted LLM service (OpenAI, Anthropic, etc.)
3. Update the LLM client to use your chosen service
4. Deploy and test!

Would you like me to help you set up any specific deployment option?
