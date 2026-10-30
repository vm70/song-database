"""Settings for the SongDB Server."""

import logging
from typing import Any, Literal, Self

import sqlalchemy
from pydantic import AnyUrl, BaseModel, Field, FilePath, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from songdb_server.keygen import verify_keys

logger = logging.getLogger(__name__)


def fetch_secret(
    secret: SecretStr | None,
    secret_env_name: str,
    secret_file: FilePath | None,
    secret_file_env_name: str,
) -> SecretStr | None:
    """Fetch a given secret's actual value.

    Args:
        secret: secret string (or none)
        secret_env_name: secret string environment variable name
        secret_file: secret file (or none)
        secret_file_env_name: secret file environment variable name
    """
    if secret is None and secret_file is None:
        logger.fatal(
            "Neither options %s nor %s were provided.",
            secret_env_name,
            secret_file_env_name,
        )
    if secret is not None and secret_file is not None:
        logger.warning(
            "Both options %s and %s were provided. Defaulting to %s",
            secret_env_name,
            secret_file_env_name,
            secret_file_env_name,
        )
    if secret_file is not None:
        return SecretStr(secret_file.read_text().strip())
    return secret


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

    def fetch_password(self) -> SecretStr | None:
        """Get The SQL password, if provided."""
        return fetch_secret(
            self.PASSWORD,
            "SONGDB__SQL__PASSWORD",
            self.PASSWORD_FILE,
            "SONGDB__SQL__PASSWORD_FILE",
        )

    def to_url(self) -> sqlalchemy.URL:
        """Get the corresponding URL from the SQL settings."""
        if self.DRIVERNAME is None:
            msg = "No SQL driver provided"
            raise ValueError(msg)
        password = self.fetch_password()
        return sqlalchemy.URL.create(
            self.DRIVERNAME,
            self.USERNAME,
            password if password is None else password.get_secret_value(),
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

    def fetch_jwt_private_key(self) -> SecretStr:
        """Get the JWT private key, if available."""
        private_key = fetch_secret(
            self.JWT_PRIVATE_KEY,
            "SONGDB__AUTH__JWT_PRIVATE_KEY",
            self.JWT_PRIVATE_KEY_FILE,
            "SONGDB__AUTH__JWT_PRIVATE_KEY_FILE",
        )
        if private_key is None:
            msg = "Could not fetch private key"
            raise ValueError(msg)
        return private_key

    def fetch_jwt_public_key(self) -> SecretStr:
        """Get the JWT public key, if available."""
        public_key = fetch_secret(
            self.JWT_PUBLIC_KEY,
            "SONGDB__AUTH__JWT_PUBLIC_KEY",
            self.JWT_PUBLIC_KEY_FILE,
            "SONGDB__AUTH__JWT_PUBLIC_KEY_FILE",
        )
        if public_key is None:
            msg = "Could not fetch public key"
            raise ValueError(msg)
        return public_key

    @model_validator(mode="after")
    def verify_jwt_keys(self) -> Self:
        """Verify JWT secrets work."""
        private_key = self.fetch_jwt_private_key()
        public_key = self.fetch_jwt_public_key()
        verify_keys(
            private_key.get_secret_value(),
            public_key.get_secret_value(),
        )
        return self


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
