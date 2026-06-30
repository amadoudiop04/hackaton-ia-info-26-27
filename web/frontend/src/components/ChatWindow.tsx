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

export function ChatWindow({ messages, loading }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="chat-window">
      {messages.map((m, i) => (
        <Message key={i} message={m} />
      ))}
      {loading && <div className="chat-window__typing">…</div>}
      <div ref={bottomRef} />
    </div>
  );
}
