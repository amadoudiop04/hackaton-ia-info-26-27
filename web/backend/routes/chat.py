"""Routes de l'API chat.

Owner: Amadou (feat/backend-api)

    POST /api/chat         -> ChatResponse
    POST /api/chat/stream  -> StreamingResponse (text/event-stream)
    GET  /api/health       -> HealthResponse
"""

from fastapi import APIRouter

from models.schemas import ChatRequest, ChatResponse, HealthResponse

router = APIRouter(prefix="/api", tags=["chat"])


@router.get("/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """Statut du serveur d'inférence (consommé par la pastille 🟢/🔴 du frontend)."""
    raise NotImplementedError


@router.post("/chat", response_model=ChatResponse)
async def post_chat(req: ChatRequest) -> ChatResponse:
    """Réponse complète (non-stream)."""
    raise NotImplementedError


@router.post("/chat/stream")
async def post_chat_stream(req: ChatRequest):
    """Réponse en streaming (StreamingResponse sur services.ollama.chat_stream)."""
    raise NotImplementedError
