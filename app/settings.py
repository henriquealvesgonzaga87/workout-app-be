from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    PROJECT_NAME: str = "Workout-app-be"
    ROOT_PATH: str = "/workout-app-be"
    PREFIX: str = "/api/v1"


@lru_cache
def get_settings():
    return Settings()
