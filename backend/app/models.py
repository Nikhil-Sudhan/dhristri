from typing import List, Optional
from pydantic import BaseModel


class UploadResponse(BaseModel):
    uploadId: str
    videoId: str
    durationSec: int


class StatusResponse(BaseModel):
    videoId: str
    status: str
    progress: int


class MinuteSlice(BaseModel):
    startSec: int
    endSec: int
    sceneText: Optional[str] = None
    audioText: Optional[str] = None
    summaryText: str


class IngestRecord(BaseModel):
    videoId: str
    slices: List[MinuteSlice]


class ChatRequest(BaseModel):
    videoId: str
    message: str


class EvidenceItem(BaseModel):
    startSec: int
    endSec: int
    score: float


class ChatResponse(BaseModel):
    answerText: str
    clipUrl: Optional[str]
    evidence: List[EvidenceItem]





