"""
Simple Pipecat Pipeline Demo
Demonstrates the frame-based architecture
"""
import asyncio
import sys

from pipecat.frames.frames import Frame, TextFrame, EndFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor


class UppercaseProcessor(FrameProcessor):
    """Converts text to uppercase"""
    
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        
        if isinstance(frame, TextFrame):
            print(f"  [Uppercase] '{frame.text}' -> '{frame.text.upper()}'")
            await self.push_frame(TextFrame(frame.text.upper()), direction)
        else:
            await self.push_frame(frame, direction)


class ReverseProcessor(FrameProcessor):
    """Reverses text"""
    
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        
        if isinstance(frame, TextFrame):
            reversed_text = frame.text[::-1]
            print(f"  [Reverse]   '{frame.text}' -> '{reversed_text}'")
            await self.push_frame(TextFrame(reversed_text), direction)
        else:
            await self.push_frame(frame, direction)


class OutputProcessor(FrameProcessor):
    """Collects and displays final output"""
    
    def __init__(self):
        super().__init__()
        self.results = []
    
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        
        if isinstance(frame, TextFrame):
            self.results.append(frame.text)
            print(f"  [Output]    '{frame.text}'")
        
        await self.push_frame(frame, direction)


async def main():
    print("\n" + "="*70)
    print(" PIPECAT PIPELINE DEMO - Frame-Based Processing")
    print("="*70)
    print("\nPipecat processes data as 'frames' through a pipeline of processors.")
    print("This demo shows: Input -> Uppercase -> Reverse -> Output\n")
    
    # Create processors
    output_proc = OutputProcessor()
    
    # Build pipeline
    pipeline = Pipeline([
        UppercaseProcessor(),
        ReverseProcessor(),
        output_proc
    ])
    
    # Create task
    task = PipelineTask(pipeline)
    
    # Send frames through pipeline
    async def send_test_data():
        await asyncio.sleep(0.1)
        
        test_inputs = [
            "hello pipecat",
            "voice ai",
            "real-time"
        ]
        
        print("Processing frames through pipeline:\n")
        
        frames = [TextFrame(text) for text in test_inputs]
        frames.append(EndFrame())
        
        await task.queue_frames(frames)
    
    # Run
    runner = PipelineRunner(handle_sigint=False)
    
    try:
        await asyncio.gather(runner.run(task), send_test_data())
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print(f" Processed {len(output_proc.results)} frames successfully!")
    print("="*70)
    print("\nPipecat is working! You can now:")
    print("  - Add AI services (STT, TTS, LLM)")
    print("  - Connect transports (WebRTC, WebSocket)")
    print("  - Build voice agents")
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
        sys.exit(1)
