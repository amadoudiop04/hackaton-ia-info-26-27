"""Client du serveur d'inférence.

Point d'intégration UNIQUE avec le backend choisi par l'équipe INFRA.
Changer de serveur (Ollama / Triton / maison) = adapter ce seul module.

API publique attendue par l'UI :
    - chat(messages, **params) -> str
    - chat_stream(messages, **params) -> Iterator[str]
    - health() -> bool
"""

from typing import Iterator

import config  # noqa: F401  (URL serveur, modèle, params par défaut)


def health() -> bool:
    """Vérifie que le serveur d'inférence est joignable."""
    raise NotImplementedError


def chat(messages: list[dict], temperature: float | None = None,
         max_tokens: int | None = None) -> str:
    """Envoie l'historique de conversation et retourne la réponse complète.

    Args:
        messages: liste de {"role": "user"|"assistant"|"system", "content": str}
        temperature: override optionnel de la créativité
        max_tokens: override optionnel de la longueur de réponse

    Returns:
        Le texte de la réponse du modèle.
    """
    raise NotImplementedError


def chat_stream(messages: list[dict], temperature: float | None = None,
                max_tokens: int | None = None) -> Iterator[str]:
    """Variante streaming : yield les tokens au fil de l'eau (UX temps réel)."""
    raise NotImplementedError
