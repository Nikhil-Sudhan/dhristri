# Dhristri

Minimal RAG-powered video insight system using OpenAI and Video-LLaMA.

## Run locally

### Backend
1. `cd backend`
2. Create venv and install: `python -m venv .venv && .venv/Scripts/activate` (Windows) then `pip install -r requirements.txt`
3. Ensure ffmpeg is on PATH
4. Set environment variables:
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `OPENAI_EMBEDDING_MODEL` (optional, defaults to `text-embedding-3-small`)
   - `OPENAI_CHAT_MODEL` (optional, defaults to `gpt-3.5-turbo`)
   - `VIDEOLLAMA_MODEL_PATH` (optional, defaults to `./models/videollama`)
   - `VIDEOLLAMA_CHECKPOINT_PATH` (optional, defaults to `./models/videollama/checkpoint`)
5. `uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm i`
3. `npm run dev`
4. Open the shown localhost URL

## Notes
- Upload a short video (<10 min). Videos are processed in 15-second chunks using Video-LLaMA for classification.
- Chat uses OpenAI GPT-3.5-turbo to generate answers from retrieved video segments.
- Video-LLaMA integration is currently a placeholder - implement actual model loading for production use.
- Requires GPU (RTX 3090 or better) for Video-LLaMA inference.



