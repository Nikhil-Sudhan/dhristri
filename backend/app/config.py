import os
from pathlib import Path
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load environment variables from project root .env if present
load_dotenv(PROJECT_ROOT / ".env")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")
# Chosen embedding size; collection already expects 768 dims
OPENAI_EMBEDDING_DIM = int(os.getenv("OPENAI_EMBEDDING_DIM", "768"))

# Video-LLaMA Configuration
VIDEOLLAMA_MODEL_PATH = os.getenv("VIDEOLLAMA_MODEL_PATH", str(PROJECT_ROOT / "models" / "videollama"))
VIDEOLLAMA_CHECKPOINT_PATH = os.getenv("VIDEOLLAMA_CHECKPOINT_PATH", str(PROJECT_ROOT / "models" / "videollama" / "checkpoint"))

# Storage Configuration
CHROMA_DIR = os.getenv("CHROMA_DIR", str(PROJECT_ROOT / "backend" / "app" / "store" / "indexes"))
MEDIA_DIR = os.getenv("MEDIA_DIR", str(PROJECT_ROOT / "backend" / "app" / "store"))


def ensure_dirs() -> None:
    Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)
    Path(MEDIA_DIR).mkdir(parents=True, exist_ok=True)
    (Path(MEDIA_DIR) / "videos").mkdir(parents=True, exist_ok=True)
    (Path(MEDIA_DIR) / "clips").mkdir(parents=True, exist_ok=True)





