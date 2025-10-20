# Google Gemini Setup Guide

## Getting Your FREE Gemini API Key

### Step 1: Get API Key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" 
4. Create a new API key
5. Copy the API key (starts with `AIza...`)

### Step 2: Set Environment Variable

#### For Local Development:
1. Copy `env.example` to `.env`
2. Replace `your_gemini_api_key_here` with your actual API key:
   ```
   GEMINI_API_KEY="AIzaSyC..."
   LLM_PROVIDER="gemini"
   ```

#### For Production Deployment:
Set the environment variable in your deployment platform:
- **Railway**: Add `GEMINI_API_KEY` in project settings
- **Render**: Add `GEMINI_API_KEY` in environment variables
- **Heroku**: Use `heroku config:set GEMINI_API_KEY=your_key`

### Step 3: Test the Integration

Run your chatbot locally:
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Visit `http://localhost:8000` and test the chatbot!

## Gemini Free Tier Limits

- **15 requests per minute**
- **1 million tokens per day**
- **32,000 tokens per request**

This is perfect for most chatbot applications!

## Switching Between Providers

To switch back to Ollama locally:
```bash
# In your .env file
LLM_PROVIDER="ollama"
```

To use Gemini in production:
```bash
# In your deployment environment
LLM_PROVIDER="gemini"
GEMINI_API_KEY="your_actual_key"
```
