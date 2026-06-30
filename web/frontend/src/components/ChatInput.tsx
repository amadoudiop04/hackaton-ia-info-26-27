// Barre de saisie (ComposerBar) : textarea + modèle/temp/tokens + envoi.
// Owner: Alexandre (feat/frontend-chat-ui)

import { useState } from "react";
import type { ChatParams } from "../types/chat";

interface Props {
  params: ChatParams;
  onParamsChange: (params: ChatParams) => void;
  onSend: (content: string) => void;
  disabled?: boolean;
}

const MODELS = ["phi3.5-financial", "phi3.5-mini", "mistral-7b", "llama3-8b"];
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
    <div className="composer">
      <textarea
        className="composer__field"
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        onKeyDown={onKeyDown}
        rows={1}
        placeholder="Écrivez votre message…"
        disabled={disabled}
      />

      <div className="composer__controls">
        <div className="ctl">
          <div className="ctl__select-wrap">
            <select
              className="ctl__select"
              value={params.model}
              onChange={(e) => onParamsChange({ ...params, model: e.target.value })}
            >
              {MODELS.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
            <span className="ctl__chevron">▾</span>
          </div>
        </div>

        <div className="ctl">
          <span className="ctl__label">Température</span>
          <div className="ctl__select-wrap">
            <select
              className="ctl__select"
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
            <span className="ctl__chevron">▾</span>
          </div>
        </div>

        <div className="ctl">
          <span className="ctl__label">Max tokens</span>
          <div className="ctl__select-wrap">
            <select
              className="ctl__select"
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
            <span className="ctl__chevron">▾</span>
          </div>
        </div>

        <div className="composer__spacer" />

        <button
          className="sendbtn"
          onClick={submit}
          disabled={disabled || !draft.trim()}
          aria-label="Envoyer"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="19" x2="12" y2="5" />
            <polyline points="5 12 12 5 19 12" />
          </svg>
        </button>
      </div>
    </div>
  );
}
