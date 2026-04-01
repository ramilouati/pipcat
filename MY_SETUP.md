# My Pipecat Setup

This is my personal fork of Pipecat with custom demos and configurations.

## What's Added

### Demo Files

1. **openrouter_chatbot.py** - Working chatbot using OpenRouter API
   - Uses Llama 3.3 70B model
   - Demonstrates streaming responses
   - Shows basic conversation flow
   
2. **demo.py** - Basic pipeline demonstration
   - Shows frame-based processing
   - Uppercase and reverse text processors
   - Good for understanding Pipecat architecture

3. **simple_test.py** - Quick verification script
   - Tests Pipecat installation
   - Verifies imports work correctly

4. **test_pipecat.py** - Pipeline processing demo
   - More detailed frame processing example
   - Shows multiple processors in action

### Documentation

- **OPENROUTER_GUIDE.md** - Complete guide for using OpenRouter
  - Model selection
  - API setup
  - Example code
  - Troubleshooting

## My Configuration

- **OpenRouter API**: Configured and working
- **Models Available**: 200+ models through OpenRouter
- **Current Model**: meta-llama/llama-3.3-70b-instruct

## Quick Start

```bash
# Install dependencies
uv sync --extra openrouter

# Run the chatbot demo
uv run openrouter_chatbot.py

# Run basic pipeline demo
uv run demo.py

# Test installation
uv run simple_test.py
```

## Environment Setup

API key is configured in `.env`:
```
OPENROUTER_API_KEY=sk-or-v1-xxxxx
```

## Repository

- **Personal Repo**: https://github.com/ramilouati/pipcat.git
- **Upstream**: https://github.com/pipecat-ai/pipecat.git

## Next Steps

- [ ] Try different OpenRouter models
- [ ] Add speech-to-text integration
- [ ] Add text-to-speech for voice output
- [ ] Explore function calling examples
- [ ] Build a custom voice assistant
- [ ] Try WebSocket transport for web apps

## Notes

- Running on Windows 10
- Python 3.12.10
- Using `uv` for package management
- Daily transport not available on Windows (WebRTC limitation)
- Using WebSocket and local transports instead
