"""
Minimal Pipecat test - just import and show version
"""
import sys
print("Python version:", sys.version)

try:
    import pipecat
    print("\n[OK] Pipecat successfully imported!")
    print(f"[OK] Pipecat version: {pipecat.__version__}")
    print(f"[OK] Pipecat location: {pipecat.__file__}")
    
    # Test basic frame imports
    from pipecat.frames.frames import TextFrame, EndFrame
    from pipecat.processors.frame_processor import FrameProcessor
    from pipecat.pipeline.pipeline import Pipeline
    
    print("\n[OK] Core components imported successfully:")
    print("  - Frames (TextFrame, EndFrame)")
    print("  - FrameProcessor")
    print("  - Pipeline")
    
    print("\n[OK] Pipecat is ready to use!")
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
