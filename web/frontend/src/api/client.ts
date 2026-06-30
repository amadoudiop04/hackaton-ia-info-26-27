// Client HTTP vers le BACKEND FastAPI (jamais Ollama directement).
// Owner: Maxime2 (feat/frontend-core-sidebar)

import type { ChatParams, Message } from "../types/chat";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

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
  const res = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: buildChatBody(messages, params),
  });
  if (!res.ok) {
    throw new Error(`Backend a répondu ${res.status} ${res.statusText}`);
  }
  const data: { role: string; content: string } = await res.json();
  return data.content;
}

/** POST /api/chat/stream -> appelle onToken pour chaque fragment reçu.
 *  Flux SSE (text/event-stream) : lignes "data: <token>", sentinelle "[DONE]". */
export async function sendChatStream(
  messages: Message[],
  params: ChatParams,
  onToken: (token: string) => void,
): Promise<void> {
  const res = await fetch(`${API_URL}/api/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: buildChatBody(messages, params),
  });
  if (!res.ok || !res.body) {
    throw new Error(`Backend a répondu ${res.status} ${res.statusText}`);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // On découpe sur les sauts de ligne ; la dernière ligne (peut-être
    // incomplète) reste dans le buffer pour le prochain chunk.
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed.startsWith("data:")) continue;

      const payload = trimmed.slice("data:".length).trim();
      if (payload === "[DONE]") return;
      if (payload) onToken(payload);
    }
  }
}
