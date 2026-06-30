# web/streamlit/ollama_client.py
import json
from collections.abc import Generator

import httpx

from config import settings


class OllamaError(Exception):
    """Erreur remontée par le client Ollama."""


def _build_payload(messages: list[dict]) -> dict:
    return {
        "model": settings.MODEL_NAME,
        "messages": messages,
        "options": {
            "temperature": settings.TEMPERATURE,
            "top_p": settings.TOP_P,
            "num_ctx": settings.NUM_CTX,
        },
    }


def chat(messages: list[dict]) -> str:
    """Envoie une conversation et retourne la réponse complète (non streamée)."""
    payload = {**_build_payload(messages), "stream": False}
    try:
        with httpx.Client(timeout=settings.REQUEST_TIMEOUT) as client:
            response = client.post(f"{settings.OLLAMA_URL}/api/chat", json=payload)
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise OllamaError(
            f"Ollama a retourné une erreur HTTP {e.response.status_code} : {e.response.text}"
        ) from e
    except httpx.RequestError as e:
        raise OllamaError(
            f"Impossible de joindre Ollama ({settings.OLLAMA_URL}) : {e}"
        ) from e

    return response.json()["message"]["content"]


def chat_stream(messages: list[dict]) -> Generator[str, None, None]:
    """Génère la réponse token par token via le streaming JSON-lines d'Ollama."""
    payload = {**_build_payload(messages), "stream": True}
    try:
        with httpx.Client(timeout=settings.REQUEST_TIMEOUT) as client:
            with client.stream("POST", f"{settings.OLLAMA_URL}/api/chat", json=payload) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    token = chunk.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if chunk.get("done"):
                        break
    except httpx.HTTPStatusError as e:
        raise OllamaError(
            f"Ollama a retourné une erreur HTTP {e.response.status_code} : {e.response.text}"
        ) from e
    except httpx.RequestError as e:
        raise OllamaError(
            f"Impossible de joindre Ollama ({settings.OLLAMA_URL}) : {e}"
        ) from e


def health() -> bool:
    """Retourne True si Ollama répond, False sinon (sans lever d'exception)."""
    try:
        with httpx.Client(timeout=settings.HEALTH_TIMEOUT) as client:
            response = client.get(f"{settings.OLLAMA_URL}/api/tags")
            return response.status_code == 200
    except Exception:
        return False
