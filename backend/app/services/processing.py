from typing import List
from pathlib import Path
import math
import subprocess
from ..config import MEDIA_DIR, ensure_dirs
from .. import models
from ..state import status_by_video, slices_by_video
from .vertex import init_clients, embed_texts
from .rag import upsert as rag_upsert
from .videollama import get_scene_description


def enqueue_processing(video_path: str, video_id: str) -> None:
    ensure_dirs()
    status_by_video[video_id] = models.StatusResponse(videoId=video_id, status="processing", progress=0)
    init_clients()
    duration = get_video_duration_sec(video_path)
    # Process in 15-second chunks instead of 60-second minutes
    chunk_size = 15
    num_chunks = max(1, math.ceil(duration / chunk_size))
    slices: list[models.MinuteSlice] = []
    
    for i in range(num_chunks):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, duration)
        
        # Process video chunk with Video-LLaMA
        scene_text, summary_text = get_scene_description(video_path, start, end)
        
        # Create slice (audioText is None since no audio processing)
        slice_item = models.MinuteSlice(
            startSec=start,
            endSec=end,
            sceneText=scene_text,
            audioText=None,  # No audio processing
            summaryText=summary_text
        )
        slices.append(slice_item)
        
        # Embed summary and upsert to vector store
        emb = embed_texts([summary_text])[0]
        rag_upsert(video_id, start, end, summary_text, emb)
        
        # Update progress
        progress = int(((i + 1) / num_chunks) * 100)
        status_by_video[video_id] = models.StatusResponse(videoId=video_id, status="processing", progress=progress)
    
    slices_by_video[video_id] = slices
    status_by_video[video_id] = models.StatusResponse(videoId=video_id, status="ready", progress=100)


def get_video_duration_sec(video_path: str) -> int:
    try:
        # Use ffprobe to get duration
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nk=1:nw=1", video_path
        ], capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        return int(duration)
    except Exception:
        return 0


def ensure_clip(video_id: str, start_sec: int) -> str:
    clips_dir = Path(MEDIA_DIR) / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    clip_path = clips_dir / f"{video_id}_{start_sec}.mp4"
    if clip_path.exists():
        return str(clip_path)
    src = Path(MEDIA_DIR) / "videos" / f"{video_id}.mp4"
    # Create 15s clip using ffmpeg (matching chunk size)
    try:
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(start_sec), "-i", str(src), "-t", "15",
            "-c:v", "libx264", "-c:a", "copy", str(clip_path)
        ], check=True, capture_output=True)
    except Exception:
        pass
    return str(clip_path)


