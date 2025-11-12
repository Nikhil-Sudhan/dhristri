from typing import List
from openai import OpenAI
from ..config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL, OPENAI_CHAT_MODEL


_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def init_clients() -> None:
    """Initialize OpenAI client (for compatibility with existing code)."""
    _get_client()


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed texts using OpenAI embeddings API."""
    try:
        client = _get_client()
        response = client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=texts
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        # Fallback to fixed-size zero vectors so app continues to function locally
        # OpenAI embeddings are typically 1536 dimensions for text-embedding-3-small
        return [[0.0] * 1536 for _ in texts]


def chat_completion(messages: List[dict], temperature: float = 0.7) -> str:
    """Generate chat completion using OpenAI GPT-3.5-turbo."""
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"Error generating response: {str(e)}"


