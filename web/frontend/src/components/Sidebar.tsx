// Panneau latéral : paramètres d'inférence, statut serveur, actions.
// Owner: Maxime2 (feat/frontend-core-sidebar)

import type { ChatParams } from "../types/chat";

interface Props {
  params: ChatParams;
  onChange: (params: ChatParams) => void;
  onClear: () => void;
}

export function Sidebar({ params, onChange, onClear }: Props) {
  // TODO: sliders temperature/maxTokens, sélecteur modèle, pastille 🟢/🔴 (health()),
  //       bouton "Nouvelle conversation" (onClear), export JSON de l'historique
  void params;
  void onChange;
  void onClear;
  return <aside className="sidebar">{/* paramètres + statut */}</aside>;
}
