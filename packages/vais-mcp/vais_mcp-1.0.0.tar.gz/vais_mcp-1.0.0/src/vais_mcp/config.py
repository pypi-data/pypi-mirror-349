from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_CLOUD_PROJECT_ID: str
    IMPERSONATE_SERVICE_ACCOUNT: Optional[str] = None
    USE_MOUNTED_SA_KEY: bool = False
    CONTAINER_SA_KEY_PATH: str = "/app/secrets/sa-key.json"

    VAIS_ENGINE_ID: str
    VAIS_LOCATION: str = "global"
    PAGE_SIZE: int = 5
    MAX_EXTRACTIVE_SEGMENT_COUNT: int = 2

    LOG_LEVEL: str = "WARNING"

    model_config = SettingsConfigDict(extra="ignore", env_ignore_empty=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
