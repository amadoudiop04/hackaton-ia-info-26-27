# web/streamlit/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    OLLAMA_URL: str = "http://localhost:11434"
    MODEL_NAME: str = "phi3.5-financial"
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.9
    NUM_CTX: int = 4096
    REQUEST_TIMEOUT: int = 120
    HEALTH_TIMEOUT: int = 5


settings = Settings()
