# TASKS — DEV WEB (Interface Chat)

Pôle de 4 développeurs. Backend **FastAPI (Python)** + Frontend **React (Vite + TS + CSS)**.
Le serveur d'inférence (Ollama) est piloté par INFRA ; le frontend ne parle **jamais**
directement à Ollama, uniquement au backend.

```
Frontend React (:5173) ──> Backend FastAPI (:8000) ──> Ollama (:11434)
```

## ★ Contrat commun (à figer EN PREMIER par Amadou)

`backend/models/schemas.py` (Pydantic) et `frontend/src/types/chat.ts` (TS) doivent
décrire la même chose :

```
POST /api/chat         { messages, temperature, max_tokens, model } → { role, content }
POST /api/chat/stream  (même body)                                  → flux de tokens
GET  /api/health                                                    → { ok, model }

Message = { role: "user" | "assistant" | "system", content: string }
```

Tant que ce contrat est respecté, les 4 lots avancent **en parallèle**.

---

## 👤 Amadou — Lead Backend & Intégration
**Branche : `feat/backend-api`**
Fichiers : `backend/main.py`, `backend/routes/chat.py`, `backend/models/schemas.py`

- [ ] Setup FastAPI + CORS (autoriser `http://localhost:5173`)
- [ ] Schemas Pydantic `Message / ChatRequest / ChatResponse / HealthResponse` → **pousser en premier**
- [ ] Route `GET /api/health`
- [ ] Route `POST /api/chat`
- [ ] Route `POST /api/chat/stream` (StreamingResponse)
- [ ] Merge final des 3 autres branches

**OK si :** `uvicorn main:app` démarre, `/docs` accessible, routes branchées sur le service.

---

## 👤 Maxime — Service Ollama (cœur d'inférence)
**Branche : `feat/backend-ollama`**
Fichiers : `backend/services/ollama.py`, `backend/config.py`, `backend/.env.example`

- [ ] `config.py` via `pydantic-settings` (OLLAMA_URL, MODEL_NAME, params)
- [ ] `chat()` → `httpx.post {OLLAMA_URL}/api/chat` (stream=false)
- [ ] `chat_stream()` → async generator sur le flux Ollama
- [ ] `health()` → `GET /api/tags` + timeout / erreurs propres

**OK si :** appel réel à Ollama renvoie une réponse. **Chemin critique — démarrer en premier.**

---

## 👤 Alexandre — Frontend UI Chat & Style
**Branche : `feat/frontend-chat-ui`**
Fichiers : `frontend/src/components/ChatWindow.tsx`, `Message.tsx`, `ChatInput.tsx`,
`styles/chat.css`, `global.css`

- [ ] `Message.tsx` : bulle user/assistant + rendu markdown
- [ ] `ChatWindow.tsx` : liste scrollable + auto-scroll en bas
- [ ] `ChatInput.tsx` : textarea + envoi (Entrée), désactivé pendant loading
- [ ] CSS : bulles, couleurs, responsive

**OK si :** conversation lisible et fluide (travail possible avec messages mockés).

---

## 👤 Maxime pontus — Frontend Setup, État & Sidebar
**Branche : `feat/frontend-core-sidebar`**
Fichiers : `frontend/` (init Vite), `src/main.tsx`, `App.tsx`, `api/client.ts`,
`hooks/useChat.ts`, `components/Sidebar.tsx`, `styles/sidebar.css`

- [ ] Init projet Vite + `npm install`
- [ ] `api/client.ts` : `fetch {VITE_API_URL}/api/chat` (+ stream)
- [ ] `useChat.ts` : state `messages`, `sendMessage`, `clear`, loading/erreur
- [ ] `Sidebar.tsx` : sliders params, sélecteur modèle, statut 🟢/🔴 (`/api/health`), reset, export JSON

**OK si :** `npm run dev` build, l'app parle au backend, params ajustables en live.

---

## Récap branches

| Dev       | Branche                       | Domaine                          |
|-----------|-------------------------------|----------------------------------|
| Amadou    | `feat/backend-api`            | Backend FastAPI + intégration    |
| Maxime    | `feat/backend-ollama`         | Service Ollama                   |
| Alexandre | `feat/frontend-chat-ui`       | UI Chat + CSS                    |
| Maxime2   | `feat/frontend-core-sidebar`  | Setup React + état + sidebar     |

## Workflow git

```bash
# 1. Amadou pousse le contrat sur main (schemas.py + types/chat.ts)
# 2. Chacun crée sa branche depuis main
git checkout main && git pull
git checkout -b feat/backend-ollama        # (exemple)
# 3. Travail + commits, puis PR vers main
# 4. Amadou merge tout et lance le test end-to-end
```

Fichiers disjoints par lot → merges triviaux.
