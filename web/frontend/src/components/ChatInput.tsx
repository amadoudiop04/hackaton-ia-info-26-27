// Zone de saisie : textarea + envoi (Entrée), désactivée pendant loading.
// Owner: Alexandre (feat/frontend-chat-ui)

interface Props {
  onSend: (content: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: Props) {
  // TODO: state local du texte, submit on Enter (Shift+Enter = nouvelle ligne)
  void onSend;
  return (
    <form className="chat-input">
      <textarea className="chat-input__field" disabled={disabled} placeholder="Votre message…" />
      <button className="chat-input__send" type="submit" disabled={disabled}>
        Envoyer
      </button>
    </form>
  );
}
