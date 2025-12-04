"""
Application settings and configuration.
"""

from os import getenv
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Langfuse settings
    langfuse_secret_key: str = Field(..., env="LANGFUSE_SECRET_KEY")
    langfuse_public_key: str = Field(..., env="LANGFUSE_PUBLIC_KEY")
    langfuse_base_url: str = Field("http://localhost:3000", env="LANGFUSE_BASE_URL")

    # OpenRouter settings
    openrouter_api_key: str = Field(..., env="OPENROUTER_API_KEY")
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "z-ai/glm-4.5-air:free"

    # Optional site settings for OpenRouter
    site_url: str | None = Field(None, env="YOUR_SITE_URL")
    site_name: str | None = Field(None, env="YOUR_SITE_NAME")

    # LLM settings
    temperature: float = 0.2

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()