"""
Video-LLaMA service for video understanding.
Processes 15-second video chunks and returns classification/summary.
"""
from typing import Optional
from pathlib import Path
import subprocess
import tempfile
import json
from ..config import VIDEOLLAMA_MODEL_PATH, VIDEOLLAMA_CHECKPOINT_PATH


_model = None
_initialized = False
LOG_PATH = Path(r"f:\dhristri\.cursor\debug.log")

# #region agent log
def _log(hypothesis_id: str, location: str, message: str, data: dict | None = None) -> None:
    try:
        payload = {
            "sessionId": "debug-session",
            "runId": "pre-fix",
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": __import__("time").time(),
        }
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception:
        # Keep silent if logging fails
        pass
# #endregion


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
    tmp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    chunk_path = tmp_file.name
    tmp_file.close()  # Avoid open-handle conflicts on Windows
    duration = end_sec - start_sec

    try:
        _log("H5", "videollama.py:63", "ffmpeg start", {"chunkPath": chunk_path, "duration": duration})
        subprocess.run(
            [
                "ffmpeg", "-y", "-ss", str(start_sec), "-i", video_path,
                "-t", str(duration), "-c:v", "libx264", "-an",
                chunk_path
            ],
            check=True,
            capture_output=True
        )
        _log("H5", "videollama.py:73", "ffmpeg complete", {"chunkPath": chunk_path})

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
        _log("H5", "videollama.py:89", "chunk cleanup success", {"chunkPath": chunk_path})

        return summary

    except Exception as e:
        # Clean up on error
        Path(chunk_path).unlink(missing_ok=True)
        _log("H5", "videollama.py:96", "chunk cleanup after error", {"chunkPath": chunk_path, "error": str(e)})
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

