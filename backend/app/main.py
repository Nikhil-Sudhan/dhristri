from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import upload, chat, status, media
from .config import ensure_dirs


app = FastAPI(title="Dhristri")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(status.router, prefix="/api")
app.include_router(media.router, prefix="/api")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.on_event("startup")
def on_startup() -> None:
    ensure_dirs()


