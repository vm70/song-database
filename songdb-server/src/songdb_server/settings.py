"""Settings for the SongDB Server."""

import logging
import secrets
from typing import Literal

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

HashType = Literal["recommended"]

logger = logging.getLogger(__name__)


def default_secret_key() -> SecretStr:
    """Function for generating a secret key for JWT token authentication."""
    logger.warning("No secret key provided. Generating secret key.")
    return SecretStr(secrets.token_hex(64))


def default_sqlalchemy_url() -> str:
    """Return the fallback SQLAlchemy URL that uses SQLite."""
    logger.warning("No SQLAlchemy URL provided. Using fallback SQLite database.")
    return "sqlite:///file:memdb1?mode=memory&cache=shared&uri=true"


class SongDBAuthSettings(BaseModel):
    """Song database authentication settings."""

    HASH_TYPE: HashType = "recommended"
    SECRET_KEY: SecretStr = Field(default_factory=default_secret_key)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class SongDBSettings(BaseSettings):
    """Song database settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SONGDB__",
        env_nested_delimiter="__",
        extra="ignore",
    )

    SQLALCHEMY_URL: str = Field(default_factory=default_sqlalchemy_url)
    AUTH: SongDBAuthSettings = Field(default_factory=SongDBAuthSettings)
