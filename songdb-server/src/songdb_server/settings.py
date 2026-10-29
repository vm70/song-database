"""Settings for the SongDB Server."""

import logging
from pathlib import Path
from typing import Literal, Self

import sqlalchemy
from pydantic import AnyUrl, BaseModel, Field, FilePath, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

HashType = Literal["recommended"]

logger = logging.getLogger(__name__)


def consolidate_secret(
    secret: SecretStr | None, secret_file: Path | None, neither_msg: str, both_msg: str
) -> SecretStr:
    """Return the consolidation of both a secret and a secret file.

    if `secret` is not None, this function returns `secret`.
    if `secret_file` is not None, this function returns `secret_file`'s contents.

    Args:
        secret: secret string
        secret_file: Path to a secret
        neither_msg: Error message when neither `secret` nor `secret_file` are provided
        both_msg: Error message when both `secret` are `secret_file` are provided

    Returns:
        consolidated secret string

    Raises:
        ValueError:
            if both secret and secret_file are provided
            if neither secret nor secret_file are provided
            if no secret can be returned
    """
    if secret is None and secret_file is None:
        raise ValueError(neither_msg)
    if secret is not None and secret_file is not None:
        raise ValueError(both_msg)
    if secret_file is not None:
        return SecretStr(secret_file.read_text().strip())
    if secret is not None:
        return secret
    msg = "Invalid secret configuration"
    raise ValueError(msg)


class SQLSettings(BaseModel):
    """SQL database settings."""

    DRIVERNAME: str
    USERNAME: str | None = None
    PASSWORD: SecretStr | None = None
    PASSWORD_FILE: FilePath | None = None
    HOST: str | None = None
    PORT: int | None = None
    DATABASE: str | None = None
    QUERY: dict[str, tuple[str] | str] = Field(default_factory=dict)

    URL: AnyUrl | None = None

    _password: SecretStr

    @model_validator(mode="after")
    def consolidate_password(self) -> Self:
        """Consolidate SQL password and SQL password file into `self.PASSWORD`."""
        self._password = consolidate_secret(
            self.PASSWORD,
            self.PASSWORD_FILE,
            "Neither SQL password nor password file provided",
            "Both SQL password and password file provided",
        )
        return self

    def to_url(self) -> str:
        """Get the corresponding URL from the SQL settings."""
        if self.URL is not None:
            return str(self.URL)
        return sqlalchemy.URL.create(
            self.DRIVERNAME,
            self.USERNAME,
            self._password.get_secret_value(),
            self.HOST,
            self.PORT,
            self.DATABASE,
            self.QUERY,
        ).render_as_string()


class AuthSettings(BaseModel):
    """Authentication settings."""

    ALGORITHM: Literal["ES256"] = "ES256"
    JWT_SECRET: SecretStr | None = None
    JWT_SECRET_FILE: FilePath | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    _jwt_secret: SecretStr

    @model_validator(mode="after")
    def consolidate_jwt_secret(self) -> Self:
        """Consolidate JWT secret and JWT secret file into `self.JWT_SECRET`."""
        self._jwt_secret = consolidate_secret(
            self.JWT_SECRET,
            self.JWT_SECRET_FILE,
            "Neither JWT secret nor secret file provided",
            "Both JWT secret and secret file provided",
        )
        return self

    @property
    def jwt_secret(self) -> SecretStr:
        """JWT secret."""
        return self._jwt_secret


class SongDBSettings(BaseSettings):
    """Song database settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SONGDB__",
        env_nested_delimiter="__",
        extra="ignore",
    )

    SQL: SQLSettings
    AUTH: AuthSettings
