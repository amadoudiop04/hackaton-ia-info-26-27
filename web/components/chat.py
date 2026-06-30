"""Composant chat : rendu de l'historique + zone de saisie utilisateur."""


def render_history(messages: list[dict]) -> None:
    """Affiche tous les messages de la conversation (bulles user/assistant)."""
    raise NotImplementedError


def render_input() -> str | None:
    """Affiche le champ de saisie et retourne le message si soumis, sinon None."""
    raise NotImplementedError
