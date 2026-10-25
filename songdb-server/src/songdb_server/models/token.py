"""API token."""

from pydantic import BaseModel


class Token(BaseModel):
    """API token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """API token data."""

    username: str | None = None
