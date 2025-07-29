# src/{{ project_slug }}/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "{{ project_name }}"
    DEBUG_MODE: bool = False
    # API_V1_STR: str = "/api/v1" # Example for API versioning

    # Database settings (example)
    # DATABASE_URL: Optional[str] = None

    # Secret key for JWT or other security features
    # SECRET_KEY: str = "a_very_secret_key"

    # model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')
    # For Pydantic v2, env_file handling is different if you want to load .env directly here.
    # Often, .env is loaded by the environment (e.g. docker-compose, systemd) or uvicorn --env-file.
    # If you want to load it here, ensure python-dotenv is installed and handle it explicitly or use
    # Pydantic's built-in support if it fits your Pydantic version and needs.

    # Example using Pydantic v2 with .env file (requires python-dotenv to be installed if not already)
    # Ensure to add `python-dotenv` to dependencies if you use this.
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8', 
        extra='ignore' # or 'allow' if you want to load extra vars
    )

# Instantiate settings
settings = Settings()

# You can then import `settings` from this module elsewhere in your app
# from {{ project_slug }}.core.config import settings 