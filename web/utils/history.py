"""Gestion de l'historique de conversation via st.session_state."""


def init_history() -> None:
    """Initialise l'historique dans la session si absent."""
    raise NotImplementedError


def add_message(role: str, content: str) -> None:
    """Ajoute un message à l'historique (role: 'user' | 'assistant' | 'system')."""
    raise NotImplementedError


def get_messages() -> list[dict]:
    """Retourne la liste des messages de la session courante."""
    raise NotImplementedError


def clear_history() -> None:
    """Réinitialise la conversation."""
    raise NotImplementedError
