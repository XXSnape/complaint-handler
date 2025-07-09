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
    """
    Конфигурация для запуска приложения.
    """

    host: str = "0.0.0.0"
    port: int = 8000


class LoggingConfig(BaseModel):
    """
    Конфигурация логирования приложения.
    """

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
        """
        Возвращает числовое значение уровня логирования.
        """
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class SentinelApi(BaseSettings):
    """
    Конфигурация для работы с API анализа тональности.
    """

    url: str = "https://api.apilayer.com/sentiment/analysis"
    key: str
    model_config = SettingsConfigDict(
        env_prefix="api_sentinel_",
    )


class HFSettings(BaseSettings):
    """
    Конфигурация для работы с Hugging Face API.
    """

    token: str
    model: str = "mistralai/Mistral-7B-Instruct-v0.3"
    model_config = SettingsConfigDict(
        env_prefix="hf_",
    )


class ApiResources(BaseModel):
    """
    Конфигурация для работы с внешними API.
    """

    sentinel: SentinelApi = SentinelApi()
    hf: HFSettings = HFSettings()


class ApiV1Prefix(BaseModel):
    """
    Префиксы для API версии 1.
    """

    prefix: str = "/v1"
    complaints: str = "/complaints"


class ApiPrefix(BaseModel):
    """
    Конфигурация префиксов для API.
    """

    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    """
    Конфигурация базы данных.
    """

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
        return "sqlite+aiosqlite:///db.sqlite3"


class Settings(BaseSettings):
    """
    Основные настройки приложения.
    """

    run: RunConfig = RunConfig()
    logging: LoggingConfig = LoggingConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig = DatabaseConfig()
    resources: ApiResources = ApiResources()


settings = Settings()
