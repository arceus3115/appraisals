"""Application settings loaded from environment (see config/env.example)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    appraisal_ai_env: str = "development"
    appraisal_ai_log_level: str = "INFO"

    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    attom_api_key: str | None = None
    regrid_api_key: str | None = None
    mapbox_access_token: str | None = None
    google_maps_api_key: str | None = None
