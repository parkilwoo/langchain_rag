from pydantic_settings import BaseSettings
from functools import lru_cache
from enum import Enum
import os

class RunMode(Enum):
    DEV = "DEV"
    PROD = "PROD"

class Settings(BaseSettings):

    # SERVICE CONFIG
    VERSION: str = "0.0.1"
    HTTP_TIMEOUT_SECOND: float = 30.0
    API_VERSION: str = "/v1"
    MODE: RunMode = RunMode.DEV

    # SWAGGER CONFIG
    SWAGGER_TITLE: str = "MY AGENT"

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )

@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
