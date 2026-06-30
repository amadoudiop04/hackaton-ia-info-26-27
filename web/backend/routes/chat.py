"""Routes de l'API chat.

Owner: Amadou (feat/backend-api)

    POST /api/chat         -> ChatResponse
    POST /api/chat/stream  -> StreamingResponse (text/plain, flux de tokens)
    GET  /api/health       -> HealthResponse
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from config import settings
from models.schemas import ChatRequest, ChatResponse, HealthResponse
from services import ollama

router = APIRouter(prefix="/api", tags=["chat"])


@router.get("/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """Statut du serveur d'inférence (consommé par la pastille 🟢/🔴 du frontend)."""
    try:
        ok = await ollama.health()
    except Exception:
        ok = False
    return HealthResponse(ok=ok, model=settings.MODEL_NAME)


@router.post("/chat", response_model=ChatResponse)
async def post_chat(req: ChatRequest) -> ChatResponse:
    """Réponse complète (non-stream)."""
    try:
        content = await ollama.chat(
            req.messages,
            temperature=req.temperature,
            max_tokens=req.max_tokens,
            model=req.model,
        )
    except Exception as exc:  # serveur d'inférence injoignable / en erreur
        raise HTTPException(status_code=502, detail=f"Inference error: {exc}") from exc
    return ChatResponse(content=content)


@router.post("/chat/stream")
async def post_chat_stream(req: ChatRequest) -> StreamingResponse:
    """Réponse en streaming (StreamingResponse sur services.ollama.chat_stream)."""
    token_stream = ollama.chat_stream(
        req.messages,
        temperature=req.temperature,
        max_tokens=req.max_tokens,
        model=req.model,
    )
    return StreamingResponse(token_stream, media_type="text/plain; charset=utf-8")
