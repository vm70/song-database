"""Settings for the SongDB Server."""

import logging
from pathlib import Path
from typing import Any, Literal, Self

import sqlalchemy
from pydantic import AnyUrl, BaseModel, Field, FilePath, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

HashType = Literal["recommended"]

logger = logging.getLogger(__name__)


def consolidate_secret(secret: SecretStr | None, secret_file: Path | None) -> SecretStr:
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
        msg = "Neither secret nor secret file provided"
        raise ValueError(msg)
    if secret is not None and secret_file is not None:
        msg = f"Both secret and secret file provided: {secret} and {secret_file}"
        raise ValueError(msg)
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
    QUERY: dict[str, tuple[str, ...] | str] = Field(default_factory=dict)
    CONNECT_ARGS: dict[str, Any] = Field(default_factory=dict)

    URL: AnyUrl | None = Field(
        default=None,
        examples=["sqlite:///file:memdb1?mode=memory&cache=shared&uri=true"],
    )
    """URL override."""

    _password: SecretStr

    @model_validator(mode="after")
    def consolidate_password(self) -> Self:
        """Consolidate SQL password and SQL password file into `self.PASSWORD`."""
        self._password = consolidate_secret(
            self.PASSWORD,
            self.PASSWORD_FILE,
        )
        return self

    @model_validator(mode="after")
    def use_override_url(self) -> Self:
        """Use the override URL."""
        if self.URL is not None:
            url = sqlalchemy.make_url(str(self.URL))
            self.DRIVERNAME = url.drivername
            self.USERNAME = url.username
            self.PASSWORD = SecretStr(url.password) if url.password else None
            self.PASSWORD_FILE = None
            self.HOST = url.host
            self.PORT = url.port
            self.DATABASE = url.database
            self.QUERY = {k: v for k, v in url.query.items()}

        return self

    def to_url(self) -> sqlalchemy.URL:
        """Get the corresponding URL from the SQL settings."""
        return sqlalchemy.URL.create(
            self.DRIVERNAME,
            self.USERNAME,
            self._password.get_secret_value(),
            self.HOST,
            self.PORT,
            self.DATABASE,
            self.QUERY,
        )


class AuthSettings(BaseModel):
    """Authentication settings."""

    ALGORITHM: Literal["HS256"] = "HS256"
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
