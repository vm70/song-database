"""OAuth2 service."""

from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from songdb_server.models.user import User
from songdb_server.settings import SongDBSettings

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/users/token")


class OAuth2Service:
    """Container class for OAuth2 objects."""

    settings: SongDBSettings
    password_hash: PasswordHash
    DUMMY_HASH: str

    def __init__(self, settings: SongDBSettings) -> None:
        """Initialize the OAuth2 service."""
        self.password_hash = PasswordHash(hashers=[Argon2Hasher()])
        self.settings = settings
        self.DUMMY_HASH = self.password_hash.hash("dummy_password")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify the given password with its hash."""
        return self.password_hash.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash the given password."""
        return self.password_hash.hash(password)

    def authenticate_user(self, user: User | None, password: str) -> User | None:
        """Authenticate the user based on the stored credentials."""
        if not user:
            self.verify_password(password, self.DUMMY_HASH)
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        """Create an access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            self.settings.AUTH.jwt_secret.get_secret_value(),
            algorithm=self.settings.AUTH.ALGORITHM,
        )

    def decode_access_token(self, token: str) -> dict:
        """Decode the access token."""
        return jwt.decode(
            token,
            key=self.settings.AUTH.jwt_secret.get_secret_value(),
        )


def get_oauth2_service(request: Request) -> OAuth2Service:
    """Get the OAuth2 service dependency."""
    return request.app.state.oauth2_service


OAuth2ServiceDep = Annotated[OAuth2Service, Depends(get_oauth2_service)]
OAuth2BearerDep = Annotated[str, Depends(OAUTH2_SCHEME)]
