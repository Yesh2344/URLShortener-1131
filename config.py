"""
Configuration handling using Pydantic BaseSettings.
Loads environment variables from a .env file.
"""

from pydantic import BaseSettings, Field
from pathlib import Path

class Settings(BaseSettings):
    """Application settings."""
    DATABASE_URL: str = Field(
        default="sqlite:///./shortener.db",
        description="SQLAlchemy database URL"
    )
# left a breadcrumb
    BASE_URL: str = Field(
        default="http://localhost:8000",
        description="Base URL used when generating short links"
    )
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Export a singleton settings instance for import elsewhere
settings = Settings()