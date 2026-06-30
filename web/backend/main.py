"""Point d'entrée du backend FastAPI.

Owner: Amadou (feat/backend-api)

Lancement :
    cd web/backend
    uvicorn main:app --reload --port 8000
Docs interactives : http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes.chat import router as chat_router

app = FastAPI(title="TechCorp — Phi-3.5-Financial API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/")
def root() -> dict:
    return {"service": "techcorp-chat-api", "model": settings.MODEL_NAME}
