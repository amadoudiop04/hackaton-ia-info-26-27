"""Configuration centralisée du backend (chargée depuis .env).

Owner: Maxime (feat/backend-ollama)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Serveur d'inférence (équipe INFRA)
    OLLAMA_URL: str = "http://localhost:11434"
    MODEL_NAME: str = "phi3.5-financial"

    # Paramètres d'inférence par défaut
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 512
    REQUEST_TIMEOUT: int = 120

    # CORS
    FRONTEND_ORIGIN: str = "http://localhost:5173"


settings = Settings()
