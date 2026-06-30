// Bulle d'un message (user / assistant), rendu markdown.
// Owner: Alexandre (feat/frontend-chat-ui)

import ReactMarkdown from "react-markdown";
import type { Message as ChatMessage } from "../types/chat";

interface Props {
  message: ChatMessage;
}

export function Message({ message }: Props) {
  return (
    <div className={`message message--${message.role}`}>
      <div className="message__bubble">
        <ReactMarkdown>{message.content}</ReactMarkdown>
      </div>
    </div>
  );
}
