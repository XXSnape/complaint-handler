import logging
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

load_dotenv()


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class SentinelApi(BaseSettings):
    url: str = "https://api.apilayer.com/sentiment/analysis"
    key: str
    model_config = SettingsConfigDict(
        env_prefix="api_sentinel_",
    )


class GoogleApi(BaseSettings):
    key: str
    model: str = "gemini-2.5-flash"
    model_config = SettingsConfigDict(
        env_prefix="api_google_",
    )


class ApiResources(BaseModel):
    sentinel: SentinelApi = SentinelApi()
    google: GoogleApi = GoogleApi()


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    complaints: str = "/complaints"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    echo: bool = False

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self) -> str:
        """
        Возвращает строку для подключения к базе данных.
        """
        return "sqlite+aiosqlite:///../db.sqlite3"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    run: RunConfig = RunConfig()
    logging: LoggingConfig = LoggingConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig = DatabaseConfig()
    resources: ApiResources = ApiResources()


settings = Settings()
