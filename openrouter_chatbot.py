"""
Simple OpenRouter Chatbot Demo
Uses OpenRouter to access various LLM models through Pipecat
"""
import asyncio
import os
from dotenv import load_dotenv

from pipecat.frames.frames import Frame, TextFrame, EndFrame, LLMMessagesFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from pipecat.services.openrouter.llm import OpenRouterLLMService

load_dotenv(override=True)


class UserInputProcessor(FrameProcessor):
    """Converts user text input into LLM messages"""
    
    def __init__(self, context: LLMContext):
        super().__init__()
        self.context = context
    
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        
        if isinstance(frame, TextFrame):
            # Add user message to context
            self.context.add_message({"role": "user", "content": frame.text})
            
            # Create LLM messages frame to trigger LLM processing
            messages_frame = LLMMessagesFrame(self.context.get_messages())
            await self.push_frame(messages_frame, direction)
        else:
            await self.push_frame(frame, direction)


class OutputProcessor(FrameProcessor):
    """Displays LLM responses"""
    
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        
        if isinstance(frame, TextFrame):
            print(f"Assistant: {frame.text}")
        
        await self.push_frame(frame, direction)


async def main():
    # Check for API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key == "...":
        print("\n" + "="*70)
        print(" ERROR: OpenRouter API Key Not Found")
        print("="*70)
        print("\nPlease add your OpenRouter API key to the .env file:")
        print("  1. Open the .env file")
        print("  2. Find the line: OPENROUTER_API_KEY=...")
        print("  3. Replace ... with your actual API key")
        print("  4. Save the file and run this script again")
        print("\nGet your API key at: https://openrouter.ai/keys")
        print()
        return
    
    print("\n" + "="*70)
    print(" PIPECAT + OPENROUTER CHATBOT DEMO")
    print("="*70)
    print("\nOpenRouter gives you access to multiple LLM providers:")
    print("  - OpenAI (GPT-4, GPT-3.5)")
    print("  - Anthropic (Claude)")
    print("  - Google (Gemini)")
    print("  - Meta (Llama)")
    print("  - And many more!")
    print("\nUsing model: meta-llama/llama-3.3-70b-instruct")
    print("-"*70)
    
    # Create LLM context
    context = LLMContext(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Keep responses concise and friendly."
            }
        ]
    )
    
    # Create OpenRouter LLM service
    llm = OpenRouterLLMService(
        api_key=api_key,
        settings=OpenRouterLLMService.Settings(
            model="meta-llama/llama-3.3-70b-instruct",  # Fast and capable model
            temperature=0.7,
        )
    )
    
    # Build pipeline
    pipeline = Pipeline([
        UserInputProcessor(context),
        llm,
        OutputProcessor()
    ])
    
    # Create task
    task = PipelineTask(pipeline)
    
    # Conversation loop
    async def chat():
        await asyncio.sleep(0.1)
        
        print("\nChat started! Type your messages (or 'quit' to exit)\n")
        
        conversation = [
            "Hello! What can you help me with?",
            "Tell me a fun fact about space",
            "What's the capital of France?",
        ]
        
        for user_input in conversation:
            print(f"\nYou: {user_input}")
            await task.queue_frames([TextFrame(user_input)])
            await asyncio.sleep(2)  # Wait for response
        
        # End the conversation
        await task.queue_frames([EndFrame()])
    
    # Run the pipeline
    runner = PipelineRunner(handle_sigint=False)
    
    try:
        await asyncio.gather(runner.run(task), chat())
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print(" Chat ended!")
    print("="*70)
    print("\nWhat you can do with OpenRouter + Pipecat:")
    print("  [OK] Build chatbots with any LLM model")
    print("  [OK] Add function calling for tool use")
    print("  [OK] Combine with STT/TTS for voice assistants")
    print("  [OK] Create multi-agent systems")
    print("  [OK] Build RAG (Retrieval Augmented Generation) apps")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
