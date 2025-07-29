from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(".").resolve()


class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str | None = None
    AZURE_OPENAI_ENDPOINT: str | None = None
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: str | None = None
    AZURE_OPENAI_API_VERSION: str | None = None

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
    )


settings = Settings()
