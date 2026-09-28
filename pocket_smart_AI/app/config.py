from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    app_name: str = "PocketSmartAI"
    app_version: str = "1.0.0"
    debug: bool = True

    database_url: str = "sqlite:///./pocketsmart.db"

    secret_key: str = "change-this-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    openai_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.
    """
    return Settings()


settings = get_settings()