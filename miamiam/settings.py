from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Application environment."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        environment (Environment): Running environment (development/production)
    """

    environment: Environment = Environment.PRODUCTION
    log_level: str = "INFO"

    # INSEE API settings
    api_url: str
    client_id: str
    client_secret: str

    model_config = SettingsConfigDict(env_prefix="M_")


settings = Settings()
