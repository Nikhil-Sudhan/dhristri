from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse
from ..config import MEDIA_DIR


router = APIRouter(tags=["media"])


@router.get("/clip")
async def get_clip(videoId: str, startSec: int):
    # Will map to generated clip file name once processing generates clips
    clips_dir = Path(MEDIA_DIR) / "clips"
    clip = clips_dir / f"{videoId}_{startSec}.mp4"
    if not clip.exists():
        return {"error": "clip_not_ready"}
    return FileResponse(str(clip), media_type="video/mp4")


