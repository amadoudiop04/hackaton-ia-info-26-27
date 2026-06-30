// Client HTTP vers le BACKEND FastAPI (jamais Ollama directement).
// Owner: Maxime2 (feat/frontend-core-sidebar)

import type { ChatParams, Message } from "../types/chat";

// @ts-ignore
const API_URL = import.meta.env?.VITE_API_URL ?? "http://localhost:8000";
void API_URL;

/** Corps de requête commun à /api/chat et /api/chat/stream.
 *  Mappe le camelCase du front vers le snake_case du contrat Pydantic. */
function buildChatBody(messages: Message[], params: ChatParams) {
  return JSON.stringify({
    messages,
    temperature: params.temperature,
    max_tokens: params.maxTokens,
    model: params.model,
  });
}

/** GET /api/health -> serveur d'inférence joignable ? */
export async function health(): Promise<boolean> {
  try {
    const res = await fetch(`${API_URL}/api/health`);
    if (!res.ok) return false;
    const data: { ok: boolean } = await res.json();
    return data.ok === true;
  } catch {
    return false;
  }
}

/** POST /api/chat -> réponse complète. */
export async function sendChat(
  messages: Message[],
  params: ChatParams,
): Promise<string> {
  void messages;
  void params;
  throw new Error("not implemented");
}

/** POST /api/chat/stream -> appelle onToken pour chaque fragment reçu.
 *  Flux SSE (text/event-stream) : lignes "data: <token>", sentinelle "[DONE]". */
export async function sendChatStream(
  messages: Message[],
  params: ChatParams,
  onToken: (token: string) => void,
): Promise<void> {
  void messages;
  void params;
  void onToken;
  throw new Error("not implemented");
}
