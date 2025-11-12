"""
Video-LLaMA service for video understanding.
Processes 15-second video chunks and returns classification/summary.
"""
from typing import Optional
from pathlib import Path
import subprocess
import tempfile
from ..config import VIDEOLLAMA_MODEL_PATH, VIDEOLLAMA_CHECKPOINT_PATH


_model = None
_initialized = False


def init_model() -> None:
    """Initialize Video-LLaMA model. Loads checkpoints on first call."""
    global _model, _initialized
    if _initialized:
        return
    
    # TODO: Implement Video-LLaMA model loading
    # This is a placeholder that will be replaced with actual Video-LLaMA integration
    # For MVP, we'll use a simple approach:
    # 1. Extract frames from video chunk
    # 2. Use Video-LLaMA to process frames
    # 3. Return summary text
    
    # Check if model path exists
    model_path = Path(VIDEOLLAMA_MODEL_PATH)
    checkpoint_path = Path(VIDEOLLAMA_CHECKPOINT_PATH)
    
    if not model_path.exists():
        # For MVP, we'll use a fallback approach
        # In production, this would load the actual Video-LLaMA model
        pass
    
    _initialized = True


def process_video_chunk(video_path: str, start_sec: int, end_sec: int) -> str:
    """
    Process a 15-second video chunk using Video-LLaMA.
    
    Args:
        video_path: Path to the full video file
        start_sec: Start time in seconds
        end_sec: End time in seconds
    
    Returns:
        Summary/classification text describing the video segment
    """
    init_model()
    
    # Extract 15-second chunk using ffmpeg
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
        chunk_path = tmp_file.name
        duration = end_sec - start_sec
        
        try:
            # Extract video chunk (no audio processing)
            subprocess.run([
                "ffmpeg", "-y", "-ss", str(start_sec), "-i", video_path,
                "-t", str(duration), "-c:v", "libx264", "-an",
                chunk_path
            ], check=True, capture_output=True)
            
            # TODO: Process with Video-LLaMA
            # For MVP placeholder, return a simple description
            # In production, this would:
            # 1. Load Video-LLaMA model
            # 2. Process video chunk
            # 3. Generate summary/classification
            
            # Placeholder: return basic description
            summary = f"Video segment from {start_sec}s to {end_sec}s. Activity detected."
            
            # Clean up temp file
            Path(chunk_path).unlink(missing_ok=True)
            
            return summary
            
        except Exception as e:
            # Clean up on error
            Path(chunk_path).unlink(missing_ok=True)
            return f"Error processing video chunk: {str(e)}"


def get_scene_description(video_path: str, start_sec: int, end_sec: int) -> tuple[str, str]:
    """
    Get scene description and summary for a video chunk.
    
    Returns:
        (sceneText, summaryText) tuple
    """
    summary = process_video_chunk(video_path, start_sec, end_sec)
    # For MVP, sceneText and summaryText are the same
    return summary, summary

