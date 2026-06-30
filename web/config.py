"""Configuration centralisée de l'interface chat.

Charge les variables d'environnement (.env) et expose les constantes
utilisées par les services et composants.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# --- Serveur d'inférence (équipe INFRA) ---
OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME: str = os.getenv("MODEL_NAME", "phi3.5-financial")

# --- Paramètres d'inférence par défaut ---
TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "512"))
REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "120"))

# --- UI ---
APP_TITLE: str = "TechCorp — Phi-3.5-Financial Chat"
SYSTEM_PROMPT: str = (
    "Tu es un assistant financier professionnel de TechCorp Industries."
)
