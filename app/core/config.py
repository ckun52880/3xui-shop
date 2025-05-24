import os
import re
import secrets
from functools import lru_cache
from typing import Optional, Self

from pydantic import (
    Field,
    IPvAnyAddress,
    PostgresDsn,
    RedisDsn,
    Secret,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import API_V1, WEBHOOK_PATH
from app.core.enums import ArchiveFormat, LogLevel

DEFAULT_BOT_HOST = "0.0.0.0"
DEFAULT_BOT_PORT = 5000
DEFAULT_BOT_WEBHOOK_PORT = 443

DEFAULT_DB_HOST = "remnashop-postgres"
DEFAULT_DB_PORT = 5432

DEFAULT_REDIS_HOST = "remnashop-redis"
DEFAULT_REDIS_PORT = 6379
DEFAULT_REDIS_NAME = "0"

DEFAULT_LOG_LEVEL = LogLevel.DEBUG
DEFAULT_LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
DEFAULT_LOG_ARCHIVE_FORMAT = ArchiveFormat.ZIP


class BotConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BOT_")

    TOKEN: Secret[str]
    SECRET_TOKEN: Secret[str] = Field(default_factory=secrets.token_hex)
    DEV_ID: int
    DOMAIN: Secret[str]
    HOST: IPvAnyAddress = DEFAULT_BOT_HOST
    PORT: int = DEFAULT_BOT_PORT
    WEBHOOK_PORT: int = DEFAULT_BOT_WEBHOOK_PORT

    @field_validator("DOMAIN")
    @classmethod
    def validate_domain(cls, field: Secret[str]) -> Secret[str]:
        DOMAIN_REGEX = r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
        domain = field.get_secret_value()
        if not domain:
            raise ValueError("Domain cannot be empty.")
        if not re.match(DOMAIN_REGEX, domain):
            raise ValueError("Invalid domain format.")
        return field

    @property
    def WEBHOOK_PATH(self) -> str:
        return f"{API_V1}{WEBHOOK_PATH}"

    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.DOMAIN.get_secret_value()}:{self.WEBHOOK_PORT}{self.WEBHOOK_PATH}"


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    HOST: str = DEFAULT_DB_HOST
    PORT: int = DEFAULT_DB_PORT
    NAME: Optional[str] = None
    USERNAME: str
    PASSWORD: Secret[str]

    def dsn(self, scheme: str = "postgresql+asyncpg") -> PostgresDsn:
        if not self.NAME:
            self.NAME = self.USERNAME
        return f"{scheme}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class RedisConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    HOST: str = DEFAULT_REDIS_HOST
    PORT: int = DEFAULT_REDIS_PORT
    NAME: str = DEFAULT_REDIS_NAME
    USERNAME: Optional[str] = None
    PASSWORD: Optional[Secret[str]] = None

    def dsn(self, scheme: str = "redis") -> RedisDsn:
        if self.USERNAME and self.PASSWORD:
            return f"{scheme}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"
        return f"{scheme}://{self.HOST}:{self.PORT}/{self.NAME}"


class LoggingConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOG_")

    LEVEL: LogLevel = DEFAULT_LOG_LEVEL
    FORMAT: str = DEFAULT_LOG_FORMAT
    ARCHIVE_FORMAT: ArchiveFormat = DEFAULT_LOG_ARCHIVE_FORMAT


class Config(BaseSettings):
    bot: BotConfig = Field(default_factory=BotConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    ORIGINS: list[str] = []

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        extra="ignore",
    )

    @classmethod
    @lru_cache
    def get(cls) -> Self:
        return cls()
