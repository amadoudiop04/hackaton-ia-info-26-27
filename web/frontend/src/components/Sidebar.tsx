// Panneau latéral : marque + nouvelle discussion + repli animé.
// Owner: Maxime2 (feat/frontend-core-sidebar)

import { useState } from "react";

interface Props {
  onClear: () => void;
}

export function Sidebar({ onClear }: Props) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside className={`sidebar${collapsed ? " sidebar--collapsed" : ""}`}>
      <div className="sidebar__brand">
        <div className="sidebar__brand-left">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path
              d="M12 0c.35 6.45 5.2 11.3 11.65 11.65C17.2 12 12.35 16.85 12 23.3 11.65 16.85 6.8 12 .35 11.65 6.8 11.3 11.65 6.45 12 0Z"
              fill="url(#tclogo)"
            />
            <defs>
              <linearGradient id="tclogo" x1="3" y1="3" x2="21" y2="21" gradientUnits="userSpaceOnUse">
                <stop stopColor="#D97757" />
                <stop offset="1" stopColor="#8E6BA8" />
              </linearGradient>
            </defs>
          </svg>
          <span className="sidebar__brand-name">TechCorp</span>
        </div>
        <button
          className="sidebar__collapse-btn"
          onClick={() => setCollapsed((c) => !c)}
          aria-label={collapsed ? "Déplier le panneau" : "Replier le panneau"}
          title={collapsed ? "Déplier" : "Replier"}
        >
          <svg
            className="sidebar__collapse"
            width="21"
            height="21"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#7a7066"
            strokeWidth="1.6"
          >
            <rect x="3.5" y="4.5" width="17" height="15" rx="3" />
            <line x1="9" y1="4.5" x2="9" y2="19.5" />
          </svg>
        </button>
      </div>

      <button className="sidebar__new" onClick={onClear} title="Nouvelle discussion">
        <svg
          width="19"
          height="19"
          viewBox="0 0 24 24"
          fill="none"
          stroke="#c0623f"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M12 20h9" />
          <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" />
        </svg>
        <span className="sidebar__new-label">Nouvelle discussion</span>
      </button>

      <div className="sidebar__spacer" />
    </aside>
  );
}
