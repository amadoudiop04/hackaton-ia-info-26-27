// Liste scrollable des messages + auto-scroll en bas.
// Owner: Alexandre (feat/frontend-chat-ui)

import type { Message as ChatMessage } from "../types/chat";
import { Message } from "./Message";

interface Props {
  messages: ChatMessage[];
  loading?: boolean;
}

export function ChatWindow({ messages, loading }: Props) {
  // TODO: ref + useEffect pour auto-scroll, indicateur "..." si loading
  return (
    <div className="chat-window">
      {messages.map((m, i) => (
        <Message key={i} message={m} />
      ))}
      {loading && <div className="chat-window__typing">…</div>}
    </div>
  );
}
