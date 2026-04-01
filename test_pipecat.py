"""
Simple Pipecat demo - demonstrates the frame-based pipeline architecture
"""
import asyncio
from loguru import logger

from pipecat.frames.frames import Frame, TextFrame, EndFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor


class UppercaseProcessor(FrameProcessor):
    """Converts text frames to uppercase"""
    
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        
        if isinstance(frame, TextFrame):
            print(f"[Uppercase] Input: {frame.text}")
            uppercase_frame = TextFrame(frame.text.upper())
            print(f"[Uppercase] Output: {uppercase_frame.text}")
            await self.push_frame(uppercase_frame, direction)
        else:
            await self.push_frame(frame, direction)


class ReverseProcessor(FrameProcessor):
    """Reverses text frames"""
    
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        
        if isinstance(frame, TextFrame):
            print(f"[Reverse] Input: {frame.text}")
            reversed_frame = TextFrame(frame.text[::-1])
            print(f"[Reverse] Output: {reversed_frame.text}")
            await self.push_frame(reversed_frame, direction)
        else:
            await self.push_frame(frame, direction)


class PrintProcessor(FrameProcessor):
    """Prints final output"""
    
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        
        if isinstance(frame, TextFrame):
            print(f"\n==> Final Result: {frame.text}\n")
        
        await self.push_frame(frame, direction)


async def main():
    print("\n" + "="*60)
    print("PIPECAT PIPELINE DEMO")
    print("="*60)
    print("\nThis demo shows how Pipecat processes data through a pipeline.")
    print("Pipeline: Input -> Uppercase -> Reverse -> Print\n")
    
    # Create a pipeline: Uppercase -> Reverse -> Print
    pipeline = Pipeline([
        UppercaseProcessor(),
        ReverseProcessor(),
        PrintProcessor()
    ])
    
    # Create a task to run the pipeline
    task = PipelineTask(pipeline)
    
    # Queue some frames to process
    async def send_frames():
        await asyncio.sleep(0.5)
        print("Sending frames through pipeline...\n")
        await task.queue_frames([
            TextFrame("hello pipecat"),
            TextFrame("this is a test"),
            TextFrame("voice ai is cool"),
            EndFrame()
        ])
    
    # Run the pipeline
    runner = PipelineRunner()
    await asyncio.gather(runner.run(task), send_frames())
    
    print("\n" + "="*60)
    print("Demo complete!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
