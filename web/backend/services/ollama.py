"""Client du serveur d'inférence Ollama.

Point d'intégration UNIQUE avec INFRA. Changer de backend (Ollama/Triton/maison)
= adapter ce seul module.

Owner: Maxime (feat/backend-ollama)
"""

import json
from collections.abc import AsyncIterator

import httpx

from config import settings
from models.schemas import Message


def _build_payload(
    messages: list[Message],
    temperature: float | None,
    max_tokens: int | None,
    model: str | None,
    *,
    stream: bool,
) -> dict:
    """Construit le corps de requête Ollama (/api/chat).

    Les paramètres None retombent sur les valeurs par défaut du .env.
    `max_tokens` est mappé sur `num_predict` (nom Ollama).
    """
    return {
        "model": model or settings.MODEL_NAME,
        "messages": [{"role": m.role, "content": m.content} for m in messages],
        "stream": stream,
        "options": {
            "temperature": temperature if temperature is not None else settings.TEMPERATURE,
            "num_predict": max_tokens if max_tokens is not None else settings.MAX_TOKENS,
        },
    }


async def health() -> bool:
    """Vérifie que le serveur d'inférence est joignable (GET /api/tags)."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{settings.OLLAMA_URL}/api/tags")
            return response.status_code == 200
    except Exception:
        return False


async def chat(messages: list[Message], temperature: float | None = None,
               max_tokens: int | None = None, model: str | None = None) -> str:
    """POST {OLLAMA_URL}/api/chat (stream=false) -> texte de la réponse."""
    payload = _build_payload(messages, temperature, max_tokens, model, stream=False)
    async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
        response = await client.post(f"{settings.OLLAMA_URL}/api/chat", json=payload)
        response.raise_for_status()
    return response.json()["message"]["content"]


async def chat_stream(messages: list[Message], temperature: float | None = None,
                      max_tokens: int | None = None,
                      model: str | None = None) -> AsyncIterator[str]:
    """POST {OLLAMA_URL}/api/chat (stream=true) -> yield les tokens au fil de l'eau.

    Ollama renvoie un flux JSON-lines ; on extrait `message.content` de chaque
    ligne et on s'arrête sur `done: true`.
    """
    payload = _build_payload(messages, temperature, max_tokens, model, stream=True)
    try:
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
            async with client.stream(
                "POST", f"{settings.OLLAMA_URL}/api/chat", json=payload
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    token = chunk.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if chunk.get("done"):
                        break
    except httpx.HTTPError as exc:
        # Le statut 200 du StreamingResponse est déjà envoyé : on ne peut plus
        # renvoyer un 502. On dégrade en émettant un dernier fragment lisible
        # côté UI plutôt que de laisser l'exception crasher l'application ASGI.
        yield f"\n\n⚠️ Serveur d'inférence injoignable ({settings.OLLAMA_URL}) : {exc}"
