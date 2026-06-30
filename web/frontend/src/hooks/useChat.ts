// Hook d'état de la conversation : messages, envoi, reset, loading/erreur.
// Owner: Maxime2 (feat/frontend-core-sidebar)

import { useState } from "react";
import type { ChatParams, Message } from "../types/chat";

export interface UseChat {
  messages: Message[];
  loading: boolean;
  error: string | null;
  sendMessage: (content: string) => Promise<void>;
  clear: () => void;
}

export function useChat(_params: ChatParams): UseChat {
  const [messages] = useState<Message[]>([]);
  const [loading] = useState(false);
  const [error] = useState<string | null>(null);

  async function sendMessage(_content: string): Promise<void> {
    throw new Error("not implemented");
  }

  function clear(): void {
    throw new Error("not implemented");
  }

  return { messages, loading, error, sendMessage, clear };
}
