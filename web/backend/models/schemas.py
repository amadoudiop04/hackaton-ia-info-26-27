"""Schemas Pydantic — CONTRAT d'API partagé backend <-> frontend.

Owner: Amadou (feat/backend-api)
⚠️ Toute modification ici doit être répercutée dans frontend/src/types/chat.ts
"""

from typing import Literal

from pydantic import BaseModel

Role = Literal["user", "assistant", "system"]


class Message(BaseModel):
    role: Role
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]
    temperature: float | None = None
    max_tokens: int | None = None
    model: str | None = None


class ChatResponse(BaseModel):
    role: Role = "assistant"
    content: str


class HealthResponse(BaseModel):
    ok: bool
    model: str
