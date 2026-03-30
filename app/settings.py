import os

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    PROJECT_NAME: str = "Workout-app-be"
    ROOT_PATH: str = "/workout-app-be"
    PREFIX: str = "/api/v1"

    DATABASE_URL: str | None = os.getenv("DATABASE_URL")


@lru_cache
def get_settings():
    return Settings()
