# OpenRouter + Pipecat Guide

## What is OpenRouter?

OpenRouter is a unified API that gives you access to 200+ AI models from different providers through a single API key. Instead of managing multiple API keys for OpenAI, Anthropic, Google, etc., you use one key for all of them.

## Setup

1. **Get your API key** at https://openrouter.ai/keys

2. **Add it to your .env file**:
   ```bash
   OPENROUTER_API_KEY=sk-or-v1-xxxxx
   ```

3. **Install OpenRouter support** (if not already installed):
   ```bash
   uv sync --extra openrouter
   ```

## What You Can Do

### 1. **Simple Text Chatbot**
Run the demo I created:
```bash
uv run openrouter_chatbot.py
```

This shows basic LLM conversation using Llama 3.3 70B.

### 2. **Available Models**

Popular models you can use with OpenRouter:

**Fast & Affordable:**
- `meta-llama/llama-3.3-70b-instruct` - Great balance
- `google/gemini-2.0-flash-exp:free` - Free!
- `anthropic/claude-3.5-haiku` - Fast Claude

**Most Capable:**
- `openai/gpt-4o` - OpenAI's best
- `anthropic/claude-3.5-sonnet` - Anthropic's best
- `google/gemini-2.0-flash-thinking-exp:free` - Reasoning model (free!)

**Specialized:**
- `deepseek/deepseek-r1` - Advanced reasoning
- `x-ai/grok-2-1212` - Grok by xAI
- `qwen/qwen-2.5-72b-instruct` - Qwen models

See all models at: https://openrouter.ai/models

### 3. **Change the Model**

In any script, just change the model parameter:

```python
llm = OpenRouterLLMService(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    settings=OpenRouterLLMService.Settings(
        model="anthropic/claude-3.5-sonnet",  # Change this!
        temperature=0.7,
    )
)
```

### 4. **Build Voice Assistants**

Combine OpenRouter with:
- **Speech-to-Text**: Deepgram, Whisper, AssemblyAI
- **Text-to-Speech**: ElevenLabs, Cartesia, OpenAI TTS
- **Transport**: WebRTC (Daily), WebSocket

Example pipeline:
```
User speaks → STT → OpenRouter LLM → TTS → User hears response
```

### 5. **Function Calling**

OpenRouter supports function calling (tool use). See example:
```bash
uv run examples/foundational/14m-function-calling-openrouter.py
```

This lets your AI:
- Call APIs
- Query databases
- Control smart devices
- Perform calculations
- And more!

### 6. **Advanced Features**

**Streaming Responses:**
Pipecat automatically handles streaming from OpenRouter, so responses come in real-time.

**Context Management:**
Use `LLMContext` to manage conversation history:
```python
context = LLMContext(
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello!"},
    ]
)
```

**Settings:**
```python
settings=OpenRouterLLMService.Settings(
    model="meta-llama/llama-3.3-70b-instruct",
    temperature=0.7,        # Creativity (0-2)
    max_tokens=1000,        # Response length
    top_p=0.9,              # Nucleus sampling
    frequency_penalty=0.0,  # Reduce repetition
)
```

## Example Projects

### Simple Q&A Bot
```python
from pipecat.services.openrouter.llm import OpenRouterLLMService

llm = OpenRouterLLMService(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    settings=OpenRouterLLMService.Settings(
        model="meta-llama/llama-3.3-70b-instruct"
    )
)
```

### Customer Support Bot
- Use function calling to query order status
- Connect to CRM systems
- Escalate to human when needed

### Voice Assistant
- Add Deepgram STT
- Add ElevenLabs TTS
- Deploy on Daily WebRTC

### Multi-Agent System
- Create multiple LLM instances
- Each with different roles/personalities
- Coordinate between them

## Cost Management

OpenRouter shows costs per request. To optimize:

1. **Use cheaper models** for simple tasks (Llama, Gemini Flash)
2. **Use expensive models** only when needed (GPT-4, Claude Sonnet)
3. **Set max_tokens** to limit response length
4. **Cache system prompts** (OpenRouter supports prompt caching)

## Next Steps

1. **Add your API key** to `.env`
2. **Run the demo**: `uv run openrouter_chatbot.py`
3. **Explore examples** in `examples/foundational/`
4. **Try different models** - just change the model name!
5. **Build something cool** 🚀

## Resources

- OpenRouter Docs: https://openrouter.ai/docs
- Pipecat Docs: https://docs.pipecat.ai
- Model List: https://openrouter.ai/models
- Pricing: https://openrouter.ai/models (shown per model)

## Troubleshooting

**"API key not found"**
- Make sure you added it to `.env`
- Check the format: `OPENROUTER_API_KEY=sk-or-v1-xxxxx`

**"Model not found"**
- Check the model name at https://openrouter.ai/models
- Use the full model ID (e.g., `openai/gpt-4o`)

**"Rate limit exceeded"**
- OpenRouter has rate limits per model
- Try a different model or wait a moment

**"Insufficient credits"**
- Add credits at https://openrouter.ai/credits
- Or use free models (marked "free" on the website)
