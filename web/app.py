"""Point d'entrée de l'interface chat Streamlit.

Orchestration : assemble sidebar + historique + saisie, et relie l'UI
au serveur d'inférence via services.inference.

Lancement :
    streamlit run app.py
"""

import streamlit as st

import config
from components import chat, sidebar
from services import inference
from utils import history


def main() -> None:
    st.set_page_config(page_title=config.APP_TITLE, layout="wide")
    st.title(config.APP_TITLE)

    # 1. Historique de session
    history.init_history()

    # 2. Paramètres (sidebar) + statut serveur
    params = sidebar.render_sidebar()

    # 3. Affichage de la conversation
    chat.render_history(history.get_messages())

    # 4. Saisie utilisateur -> appel modèle -> réponse
    user_message = chat.render_input()
    if user_message:
        history.add_message("user", user_message)
        answer = inference.chat(history.get_messages(), **params)
        history.add_message("assistant", answer)
        st.rerun()


if __name__ == "__main__":
    main()
