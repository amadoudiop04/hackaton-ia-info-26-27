# DEV WEB — Interface Chat TechCorp

Interface de chat pour dialoguer avec le modèle **Phi-3.5-Financial**.
Architecture découplée : **backend Python (FastAPI)** qui pilote le serveur
d'inférence Ollama, **frontend React (Vite + TS + CSS)** qui parle au backend.

```
Navigateur ──> Frontend React (:5173) ──> Backend FastAPI (:8000) ──> Ollama (:11434)
```

## Architecture

```
web/
├── backend/                      # Python — FastAPI
│   ├── main.py                   # app + CORS + montage des routes
│   ├── config.py                 # .env : OLLAMA_URL, MODEL_NAME, params
│   ├── routes/chat.py            # POST /api/chat · /api/chat/stream · GET /api/health
│   ├── services/ollama.py        # client Ollama (httpx)
│   ├── models/schemas.py         # ★ contrat : Message, ChatRequest, ChatResponse
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/                     # React + Vite + TS + CSS
    ├── package.json · vite.config.ts · tsconfig.json · index.html
    ├── .env.example              # VITE_API_URL=http://localhost:8000
    └── src/
        ├── main.tsx · App.tsx
        ├── types/chat.ts         # ★ types alignés sur schemas.py
        ├── api/client.ts         # appelle le BACKEND
        ├── hooks/useChat.ts      # état conversation + envoi
        ├── components/ ChatWindow · Message · ChatInput · Sidebar
        └── styles/ global · chat · sidebar (.css)
```

## Démarrage

### Backend (terminal 1)
```bash
cd web/backend
python -m venv .venv && .venv\Scripts\activate     # Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
```
Docs interactives : http://localhost:8000/docs

### Frontend (terminal 2)
```bash
cd web/frontend
npm install
cp .env.example .env
npm run dev
```
Interface : http://localhost:5173

## Contrat d'API (frontière backend ↔ frontend)

```
POST /api/chat         { messages, temperature, max_tokens, model } → { role, content }
POST /api/chat/stream  (même body)                                  → flux de tokens
GET  /api/health                                                    → { ok, model }

Message = { role: "user"|"assistant"|"system", content: string }
```

Les types `frontend/src/types/chat.ts` doivent rester alignés sur
`backend/models/schemas.py`.

## Répartition des tâches

Voir [TASKS.md](../TASKS.md) à la racine du dépôt.
