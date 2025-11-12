from fastapi import APIRouter
from .. import models
from ..state import slices_by_video
from ..services.vertex import embed_texts, chat_completion
from ..services.rag import search
from ..services.processing import ensure_clip


router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=models.ChatResponse)
async def chat(req: models.ChatRequest):
    # Embed query and search vector store
    q_emb = embed_texts([req.message])[0]
    res = search(req.videoId, q_emb, k=5)
    
    best_start = None
    best_end = None
    contexts = []
    
    if res and res.get("metadatas") and len(res["metadatas"]) > 0:
        # Chroma returns metadatas as list of lists (one per query embedding)
        # Since we query with one embedding, get the first list
        metadata_list = res["metadatas"][0] if res["metadatas"] else []
        
        # Get top results for context
        for i, md in enumerate(metadata_list):
            if md:
                start = int(md.get("startSec", 0))
                end = int(md.get("endSec", 0))
                if i == 0:
                    best_start = start
                    best_end = end
                
                # Get summary text from slices or use document text
                summary_text = None
                for s in slices_by_video.get(req.videoId, []):
                    if s.startSec == start:
                        summary_text = s.summaryText
                        break
                
                # Fallback to document text if slice not found
                if not summary_text and res.get("documents") and len(res["documents"]) > 0:
                    doc_list = res["documents"][0]
                    if i < len(doc_list):
                        summary_text = doc_list[i]
                
                if summary_text:
                    contexts.append(f"[{start}s-{end}s] {summary_text}")
    
    # Generate answer using OpenAI GPT-3.5-turbo
    if contexts:
        prompt = f"""Based on the following video segment summaries, answer the user's question concisely.

Video segments:
{chr(10).join(contexts)}

User question: {req.message}

Provide a short, direct answer based on the video content:"""
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions about video content based on provided summaries."},
            {"role": "user", "content": prompt}
        ]
        answer = chat_completion(messages)
    else:
        answer = "I couldn't find relevant video segments to answer your question."
    
    clip_url = None
    if best_start is not None:
        path = ensure_clip(req.videoId, best_start)
        # Served by /api/clip
        clip_url = f"/api/clip?videoId={req.videoId}&startSec={best_start}"
    
    evidence = []
    if best_start is not None:
        evidence = [models.EvidenceItem(startSec=best_start, endSec=best_end or (best_start + 15), score=1.0)]
    
    return models.ChatResponse(answerText=answer, clipUrl=clip_url, evidence=evidence)


