// Zone de saisie : textarea + envoi (Entrée), désactivée pendant loading.
// Owner: Alexandre (feat/frontend-chat-ui)

import { useState, KeyboardEvent, FormEvent } from "react";

interface Props {
  onSend: (content: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: Props) {
  const [content, setContent] = useState("");

  const handleSubmit = (e?: FormEvent) => {
    e?.preventDefault();
    if (content.trim() && !disabled) {
      onSend(content.trim());
      setContent("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <textarea 
        className="chat-input__field" 
        value={content}
        onChange={(e) => setContent(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled} 
        placeholder="Votre message…" 
        rows={1}
      />
      <button className="chat-input__send" type="submit" disabled={disabled || !content.trim()}>
        Envoyer
      </button>
    </form>
  );
}
