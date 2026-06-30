// Types alignés sur backend/models/schemas.py — CONTRAT partagé.
// Owner: Amadou (figé en premier). Toute évolution doit suivre les schemas Pydantic.

export type Role = "user" | "assistant" | "system";

export interface Message {
  role: Role;
  content: string;
}

export interface ChatParams {
  temperature: number;
  maxTokens: number;
  model: string;
}
