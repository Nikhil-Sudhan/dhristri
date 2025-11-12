from fastapi import APIRouter
from .. import models
from ..state import status_by_video


router = APIRouter(tags=["status"])


@router.get("/status/{videoId}", response_model=models.StatusResponse)
async def get_status(videoId: str):
    # In-memory default until wired to processing updates
    return status_by_video.get(videoId, models.StatusResponse(videoId=videoId, status="queued", progress=0))


