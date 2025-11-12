from pathlib import Path
import uuid
from fastapi import APIRouter, UploadFile, BackgroundTasks
from .. import models
from ..config import MEDIA_DIR, ensure_dirs
from ..services.processing import enqueue_processing, get_video_duration_sec


router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=models.UploadResponse)
async def upload_video(file: UploadFile, background_tasks: BackgroundTasks):
    ensure_dirs()
    video_id = uuid.uuid4().hex
    upload_id = uuid.uuid4().hex
    videos_dir = Path(MEDIA_DIR) / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)
    dest = videos_dir / f"{video_id}.mp4"
    content = await file.read()
    dest.write_bytes(content)
    duration = get_video_duration_sec(str(dest))
    background_tasks.add_task(enqueue_processing, str(dest), video_id)
    return models.UploadResponse(uploadId=upload_id, videoId=video_id, durationSec=duration)


