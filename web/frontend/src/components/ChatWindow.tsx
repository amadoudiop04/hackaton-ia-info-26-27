// Liste scrollable des messages + auto-scroll en bas.
// Owner: Alexandre (feat/frontend-chat-ui)

import { useEffect, useRef } from "react";
import type { Message as ChatMessage } from "../types/chat";
import { Message } from "./Message";

interface Props {
  messages: ChatMessage[];
  loading?: boolean;
  model: string;
}

export function ChatWindow({ messages, loading, model }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll en bas à chaque nouveau message / token reçu.
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const isEmpty = messages.length === 0;

  return (
    <div className="chat-window scroll">
      {isEmpty ? (
        <div className="chat-empty">
          <div className="chat-empty__title">Démarrez la conversation</div>
          <div className="chat-empty__hint">Posez une question à {model}</div>
        </div>
      ) : (
        <div className="chat-window__list">
          {messages.map((m, i) => (
            <Message key={i} message={m} />
          ))}
          <div ref={bottomRef} />
        </div>
      )}
    </div>
  );
}
