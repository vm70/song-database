"""Settings for the SongDB Server."""

import logging
from pathlib import Path
from typing import Any, Literal, Self

import sqlalchemy
from pydantic import AnyUrl, BaseModel, Field, FilePath, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

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
        msg = "Both secret and secret file provided"
        raise ValueError(msg)
    if secret_file is not None:
        return SecretStr(secret_file.read_text().strip())
    if secret is not None:
        return secret
    msg = "Invalid secret configuration"
    raise ValueError(msg)


class SQLSettings(BaseModel):
    """SQL database settings."""

    DRIVERNAME: str | None = None
    """Database backend and driver name."""
    USERNAME: str | None = None
    """Username of the database user."""
    PASSWORD: SecretStr | None = None
    """Password of the database user.

    This is not necessary if a password file is specified.
    """
    PASSWORD_FILE: FilePath | None = None
    """File containing the password of the database user.

    This is not necessary if a password is specified.
    """
    HOST: str | None = None
    """Hostname or IP number. May also be a data source for some drivers."""
    PORT: int | None = None
    """Integer port number."""
    DATABASE: str | None = None
    """Database name."""
    QUERY: dict[str, tuple[str, ...] | str] = Field(default_factory=dict)
    """HTTP query parameters passed to the SQL dialect and/or the DBAPI upon connect."""
    CONNECT_ARGS: dict[str, Any] = Field(default_factory=dict)
    """SQLAlchemy connection arguments."""

    URL_OVERRIDE: AnyUrl | None = Field(
        default=None,
        examples=["sqlite:///file:memdb1?mode=memory&cache=shared&uri=true"],
    )
    """URL override.

    If this is provided, then all other settings values (except for
    CONNECT_ARGS) will be overwritten and auto-populated.
    """

    _consolidated_password: SecretStr

    @model_validator(mode="after")
    def use_override_url(self) -> Self:
        """Use the override URL."""
        if self.URL_OVERRIDE is not None:
            url = sqlalchemy.make_url(str(self.URL_OVERRIDE))
            self.DRIVERNAME = url.drivername
            self.USERNAME = url.username
            self.PASSWORD = SecretStr(url.password) if url.password else None
            self.PASSWORD_FILE = None
            self.HOST = url.host
            self.PORT = url.port
            self.DATABASE = url.database
            self.QUERY = {k: v for k, v in url.query.items()}
        return self

    @model_validator(mode="after")
    def consolidate_password(self) -> Self:
        """Consolidate SQL password and SQL password file into `self._password`."""
        self._consolidated_password = consolidate_secret(
            self.PASSWORD,
            self.PASSWORD_FILE,
        )
        return self

    def to_url(self) -> sqlalchemy.URL:
        """Get the corresponding URL from the SQL settings."""
        if self.DRIVERNAME is None:
            msg = "No SQL driver provided"
            raise ValueError(msg)
        return sqlalchemy.URL.create(
            self.DRIVERNAME,
            self.USERNAME,
            self._consolidated_password.get_secret_value(),
            self.HOST,
            self.PORT,
            self.DATABASE,
            self.QUERY,
        )


class AuthSettings(BaseModel):
    """Authentication settings."""

    ALGORITHM: Literal["ES256"] = "ES256"
    """JWT encryption algorithm."""
    JWT_PRIVATE_KEY: SecretStr | None = None
    """JWT private key for encryption.

    This is not necessary if a private key file is specified.
    """
    JWT_PRIVATE_KEY_FILE: FilePath | None = None
    """File containing the JWT private key for encryption.

    This is not necessary if a private key is specified.
    """
    JWT_PUBLIC_KEY: SecretStr | None = None
    """JWT public key for encryption.

    This is not necessary if a public key file is specified.
    """
    JWT_PUBLIC_KEY_FILE: FilePath | None = None
    """File containing the JWT public key for encryption.

    This is not necessary if a public key is specified.
    """
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    """JWT default expiration time, in minutes."""

    _consolidated_jwt_private_key: SecretStr
    _consolidated_jwt_public_key: SecretStr

    @model_validator(mode="after")
    def consolidate_jwt_secret(self) -> Self:
        """Consolidate JWT secrets / files."""
        self._consolidated_jwt_private_key = consolidate_secret(
            self.JWT_PRIVATE_KEY,
            self.JWT_PRIVATE_KEY_FILE,
        )
        self._consolidated_jwt_public_key = consolidate_secret(
            self.JWT_PUBLIC_KEY,
            self.JWT_PUBLIC_KEY_FILE,
        )
        return self

    @property
    def jwt_private_key(self) -> SecretStr:
        """JWT private key."""
        return self._consolidated_jwt_private_key

    @property
    def jwt_public_key(self) -> SecretStr:
        """JWT public key."""
        return self._consolidated_jwt_public_key


class ApiSettings(BaseModel):
    """Song Database API settings."""

    SHOW_DOCS: bool = False
    """Whether to show API documentation at `/docs`."""
    SHOW_REDOC: bool = False
    """Whether to show API documentation at `/redoc`."""
    SHOW_OPENAPI_JSON: bool = False
    """Whether to show the OpenAPI JSON documentation at `/openapi.json`."""


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
    API: ApiSettings
