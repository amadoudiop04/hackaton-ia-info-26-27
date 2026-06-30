// Hook d'état de la conversation : messages, envoi, reset, loading/erreur.
// Owner: Maxime2 (feat/frontend-core-sidebar)

import { useCallback, useState } from "react";
import { sendChatStream } from "../api/client";
import type { ChatParams, Message } from "../types/chat";

export interface UseChat {
  messages: Message[];
  loading: boolean;
  error: string | null;
  sendMessage: (content: string) => Promise<void>;
  clear: () => void;
}

export function useChat(params: ChatParams): UseChat {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (content: string): Promise<void> => {
      const trimmed = content.trim();
      if (!trimmed || loading) return;

      setError(null);
      setLoading(true);

      // Historique envoyé au backend = conversation actuelle + nouveau message user.
      const userMessage: Message = { role: "user", content: trimmed };
      const history = [...messages, userMessage];

      // On affiche le message user + une bulle assistant vide qu'on remplit au fil du flux.
      setMessages([...history, { role: "assistant", content: "" }]);

      try {
        await sendChatStream(history, params, (token) => {
          setMessages((prev) => {
            const next = [...prev];
            const last = next[next.length - 1];
            next[next.length - 1] = { ...last, content: last.content + token };
            return next;
          });
        });
      } catch (e) {
        setError(e instanceof Error ? e.message : "Erreur inconnue");
        // En cas d'échec, on retire la bulle assistant restée vide.
        setMessages((prev) => {
          const last = prev[prev.length - 1];
          if (last?.role === "assistant" && last.content === "") {
            return prev.slice(0, -1);
          }
          return prev;
        });
      } finally {
        setLoading(false);
      }
    },
    [messages, params, loading],
  );

  const clear = useCallback((): void => {
    setMessages([]);
    setError(null);
  }, []);

  return { messages, loading, error, sendMessage, clear };
}
