"""API router for users."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from songdb_server.api.services.authentication import (
    OAuth2BearerDep,
    OAuth2ServiceDep,
)
from songdb_server.api.services.database import SessionDep
from songdb_server.models.token import Token, TokenData
from songdb_server.models.user import (
    User,
    UserCreateRequest,
    UserListResponse,
    UserResponse,
)
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

users_router = APIRouter(prefix="/users", tags=["users"])


def get_user(username: str, session: SessionDep) -> User | None:
    """Get the given user by username."""
    return session.scalars(select(User).filter_by(username=username)).first()


async def get_current_user(
    token: OAuth2BearerDep,
    session: SessionDep,
    oauth2_service: OAuth2ServiceDep,
) -> User:
    """Get the current user from a given JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = oauth2_service.decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError as e:
        raise credentials_exception from e
    user = get_user(token_data.username or "", session)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get the current active user.

    Raises:
        HTTPException: if the user is inactive

    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


CurrentActiveUserDep = Annotated[User, Depends(get_current_active_user)]


@users_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
    oauth2_service: OAuth2ServiceDep,
) -> Token:
    """Get the login access token for the given user."""
    user = oauth2_service.authenticate_user(
        get_user(form_data.username, session), form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = oauth2_service.create_access_token(
        data={"sub": user.username},
    )
    return Token(access_token=access_token, token_type="bearer")  # noqa: S106


@users_router.post("")
def add_user(
    user_in: UserCreateRequest,
    oauth2_service: OAuth2ServiceDep,
    session: SessionDep,
) -> UserResponse:
    """Add a new user."""
    user = User(
        username=user_in.username,
        hashed_password=oauth2_service.get_password_hash(user_in.password),
    )
    try:
        session.add(user)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    session.refresh(user)

    return UserResponse(uuid=user.uuid, username=user.username)


@users_router.get("/me")
async def get_user_info(current_active_user: CurrentActiveUserDep) -> UserResponse:
    """Get information about the current user."""
    return UserResponse.from_db_entry(current_active_user)


@users_router.delete("/me")
async def deactivate_user(
    current_active_user: CurrentActiveUserDep, session: SessionDep
) -> UserResponse:
    """Deactivate the current user."""
    current_active_user.is_active = False
    session.commit()
    session.refresh(current_active_user)
    return UserResponse.from_db_entry(current_active_user)


@users_router.get("", dependencies=[Depends(get_current_active_user)])
def get_users(
    session: SessionDep,
) -> UserListResponse:
    """Get the list of all current users."""
    return UserListResponse.from_db_entries(session.exec(select(User)).all())
