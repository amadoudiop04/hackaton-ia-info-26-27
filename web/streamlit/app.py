# web/streamlit/app.py
import streamlit as st

from config import settings
from ollama_client import OllamaError, chat_stream, health

# ── Configuration de la page ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Finance Assistant",
    page_icon="💹",
    layout="centered",
)

# ── Health check au démarrage ─────────────────────────────────────────────────
if "ollama_ok" not in st.session_state:
    st.session_state.ollama_ok = health()

if not st.session_state.ollama_ok:
    st.error(
        f"❌ Impossible de joindre Ollama sur **{settings.OLLAMA_URL}**.\n\n"
        "Vérifie qu'Ollama est lancé (`ollama serve`) et que le modèle est chargé."
    )
    if st.button("🔄 Réessayer"):
        st.session_state.ollama_ok = health()
        st.rerun()
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("💹 Finance Assistant")
    st.caption(f"Modèle : `{settings.MODEL_NAME}`")
    st.divider()
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()

# ── Initialisation de l'historique ───────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages: list[dict] = []

# ── Affichage de l'historique ─────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Saisie utilisateur ────────────────────────────────────────────────────────
user_input = st.chat_input("Pose ta question financière…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            for token in chat_stream(st.session_state.messages):
                full_response += token
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
        except OllamaError as e:
            placeholder.error(f"⚠️ Erreur Ollama : {e}")
