"""Client du serveur d'inférence Ollama.

Point d'intégration UNIQUE avec INFRA. Changer de backend (Ollama/Triton/maison)
= adapter ce seul module.

Owner: Maxime (feat/backend-ollama)
"""

from collections.abc import AsyncIterator

from config import settings
from models.schemas import Message


async def health() -> bool:
    """Vérifie que le serveur d'inférence est joignable (GET /api/tags)."""
    raise NotImplementedError


async def chat(messages: list[Message], temperature: float | None = None,
               max_tokens: int | None = None, model: str | None = None) -> str:
    """POST {OLLAMA_URL}/api/chat (stream=false) -> texte de la réponse."""
    raise NotImplementedError


async def chat_stream(messages: list[Message], temperature: float | None = None,
                      max_tokens: int | None = None,
                      model: str | None = None) -> AsyncIterator[str]:
    """POST {OLLAMA_URL}/api/chat (stream=true) -> yield les tokens au fil de l'eau."""
    raise NotImplementedError
    yield  # marque la fonction comme async generator
