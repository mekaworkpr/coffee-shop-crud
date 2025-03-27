from enum import Enum
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

CURRENT_FILE = Path(__file__).resolve()
SRC_DIR = CURRENT_FILE.parent.parent
BASE_DIR = SRC_DIR.parent


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"


class Settings(BaseSettings):
    PROJECT_NAME: str = "Coffee Shop"

    UVICORN_HOST: str = "localhost"
    UVICORN_PORT: int = 8000
    UVICORN_WORKERS_COUNT: int = 1
    UVICORN_RELOAD: bool = False

    LOG_LEVER: LogLevel = LogLevel.INFO
    ENVIRONMENT: Literal["dev", "prod", "pytest"] = "dev"

    DATABASE_URL: str
    DB_ECHO: bool = False

    JWT_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.joinpath(".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()  # type: ignore
