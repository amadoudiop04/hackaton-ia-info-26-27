// Zone de saisie : textarea + réglages temp/tokens + envoi (Entrée).
// Owner: Alexandre (feat/frontend-chat-ui)

import { useState } from "react";
import type { ChatParams } from "../types/chat";

interface Props {
  params: ChatParams;
  onParamsChange: (params: ChatParams) => void;
  onSend: (content: string) => void;
  disabled?: boolean;
}

// Options des menus du composer (cf. design).
const TEMPERATURES = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5];
const MAX_TOKENS = [64, 128, 256, 512, 1024, 2048, 4096];

export function ChatInput({ params, onParamsChange, onSend, disabled }: Props) {
  const [draft, setDraft] = useState("");

  function submit() {
    const text = draft.trim();
    if (!text || disabled) return;
    onSend(text);
    setDraft("");
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  return (
    <footer className="composer">
      <div className="composer__box">
        <textarea
          className="composer__field"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={onKeyDown}
          rows={1}
          placeholder="Votre message…"
          disabled={disabled}
        />

        <div className="composer__controls">
          <div className="composer__chip">
            <span className="composer__chip-label">Température</span>
            <div className="composer__chip-select-wrap">
              <select
                className="composer__chip-select"
                value={params.temperature}
                onChange={(e) =>
                  onParamsChange({ ...params, temperature: parseFloat(e.target.value) })
                }
              >
                {TEMPERATURES.map((t) => (
                  <option key={t} value={t}>
                    {t.toFixed(1)}
                  </option>
                ))}
              </select>
              <span className="composer__chip-chevron">▾</span>
            </div>
          </div>

          <div className="composer__chip">
            <span className="composer__chip-label">Max tokens</span>
            <div className="composer__chip-select-wrap">
              <select
                className="composer__chip-select"
                value={params.maxTokens}
                onChange={(e) =>
                  onParamsChange({ ...params, maxTokens: parseInt(e.target.value, 10) })
                }
              >
                {MAX_TOKENS.map((n) => (
                  <option key={n} value={n}>
                    {n}
                  </option>
                ))}
              </select>
              <span className="composer__chip-chevron">▾</span>
            </div>
          </div>

          <div className="composer__spacer" />

          <button className="composer__send" onClick={submit} disabled={disabled}>
            Envoyer
          </button>
        </div>
      </div>
    </footer>
  );
}
