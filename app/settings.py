import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    PROJECT_NAME: str = "Workout-app-be"
    ROOT_PATH: str = "/workout-app-be"
    PREFIX: str = "/api/v1"

    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    REDIS_HOST: str | None = os.getenv('REDIS_HOST')
    REDIS_PORT: int | None = int(os.getenv('REDIS_PORT'))
    REDIS_DB: int | None = int(os.getenv('REDIS_DB'))
    REDIS_DECODE_RESPONSES: bool = True


@lru_cache
def get_settings():
    return Settings()
