"""Composant sidebar : paramètres d'inférence et état du serveur."""


def render_sidebar() -> dict:
    """Affiche le panneau latéral (modèle, température, max_tokens, statut).

    Returns:
        dict des paramètres choisis par l'utilisateur, p.ex.
        {"temperature": 0.7, "max_tokens": 512}
    """
    raise NotImplementedError
