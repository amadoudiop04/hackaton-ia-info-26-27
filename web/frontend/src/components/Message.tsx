// Bulle d'un message. User = bulle beige ; assistant = icône + texte serif.
// Owner: Alexandre (feat/frontend-chat-ui)

import ReactMarkdown from "react-markdown";
import type { Message as ChatMessage } from "../types/chat";

interface Props {
  message: ChatMessage;
}

function BotAvatar() {
  return (
    <svg className="message__avatar" width="25" height="25" viewBox="0 0 24 24" fill="none">
      <path
        d="M12 0c.3 6.4 5.3 11.4 11.7 11.7C17.3 12 12.3 17 12 23.4 11.7 17 6.7 12 .3 11.7 6.7 11.4 11.7 6.4 12 0Z"
        fill="url(#gem2)"
      />
      <defs>
        <linearGradient id="gem2" x1="2" y1="3" x2="22" y2="21" gradientUnits="userSpaceOnUse">
          <stop stopColor="#D97757" />
          <stop offset="0.55" stopColor="#B0688F" />
          <stop offset="1" stopColor="#6B7FB3" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export function Message({ message }: Props) {
  if (message.role === "user") {
    return (
      <div className="message message--user">
        <div className="message__user-bubble">{message.content}</div>
      </div>
    );
  }

  return (
    <div className="message message--assistant">
      <BotAvatar />
      <div className="message__bot-text">
        <ReactMarkdown>{message.content}</ReactMarkdown>
      </div>
    </div>
  );
}
