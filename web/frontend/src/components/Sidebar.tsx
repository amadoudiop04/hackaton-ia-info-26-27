// Panneau latéral : statut serveur, sélecteur de modèle, actions.
// Owner: Maxime2 (feat/frontend-core-sidebar)

import { useEffect, useState } from "react";
import { health } from "../api/client";
import type { ChatParams, Message } from "../types/chat";

interface Props {
  params: ChatParams;
  messages: Message[];
  onChange: (params: ChatParams) => void;
  onClear: () => void;
}

// Modèles proposés dans le sélecteur (cf. design).
const MODELS = ["phi3.5-financial", "phi3.5-mini", "mistral-7b", "llama3-8b"];

export function Sidebar({ params, messages, onChange, onClear }: Props) {
  // null = pas encore vérifié, true = 🟢, false = 🔴.
  const [online, setOnline] = useState<boolean | null>(null);

  // Sonde /api/health au montage puis toutes les 5 s pour la pastille de statut.
  useEffect(() => {
    let active = true;
    const check = async () => {
      const ok = await health();
      if (active) setOnline(ok);
    };
    check();
    const id = setInterval(check, 5000);
    return () => {
      active = false;
      clearInterval(id);
    };
  }, []);

  // Télécharge l'historique courant en fichier JSON.
  function exportJson() {
    const blob = new Blob([JSON.stringify(messages, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `conversation-${new Date().toISOString().slice(0, 19)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  const statusModifier =
    online === null ? "unknown" : online ? "on" : "off";
  const statusText =
    online === null ? "Vérification…" : online ? "Connecté" : "Déconnecté";

  return (
    <aside className="sidebar">
      <div className="sidebar__status">
        <span className={`sidebar__status-dot sidebar__status-dot--${statusModifier}`} />
        <span className="sidebar__status-text">{statusText}</span>
      </div>

      <div className="sidebar__section">
        <div className="sidebar__label">Modèle</div>
        <div className="sidebar__select-wrap">
          <select
            className="sidebar__select"
            value={params.model}
            onChange={(e) => onChange({ ...params, model: e.target.value })}
          >
            {MODELS.map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>
          <span className="sidebar__chevron">▾</span>
        </div>
      </div>

      <div className="sidebar__spacer" />

      <button className="sidebar__btn" onClick={onClear}>
        <span className="sidebar__btn-icon">+</span> Nouvelle conversation
      </button>
      <button
        className="sidebar__btn sidebar__btn--ghost"
        onClick={exportJson}
        disabled={messages.length === 0}
      >
        ↓ Exporter JSON
      </button>
    </aside>
  );
}
