// Client HTTP vers le BACKEND FastAPI (jamais Ollama directement).
// Owner: Maxime2 (feat/frontend-core-sidebar)

import type { ChatParams, Message } from "../types/chat";

// @ts-ignore
const API_URL = import.meta.env?.VITE_API_URL ?? "http://localhost:8000";
void API_URL;

/** GET /api/health -> serveur d'inférence joignable ? */
export async function health(): Promise<boolean> {
  throw new Error("not implemented");
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

/** POST /api/chat/stream -> appelle onToken pour chaque fragment reçu. */
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
