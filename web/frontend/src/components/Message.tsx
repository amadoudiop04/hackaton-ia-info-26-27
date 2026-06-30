// Bulle d'un message (user / assistant), rendu markdown.
// Owner: Alexandre (feat/frontend-chat-ui)

import type { Message as ChatMessage } from "../types/chat";

interface Props {
  message: ChatMessage;
}

export function Message({ message }: Props) {
  // TODO: bulle stylée selon message.role + <ReactMarkdown>{message.content}</ReactMarkdown>
  return <div className={`message message--${message.role}`}>{message.content}</div>;
}
