"""User models."""

from collections.abc import Sequence
from typing import Self
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class BaseUser(SQLModel):
    """Base user class."""

    username: str = Field(unique=True)


class UserCreateRequest(BaseUser):
    """User creation request."""

    password: str


class User(BaseUser, table=True):
    """User entry in the database."""

    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    """The UUID of the user."""

    is_active: bool = True
    hashed_password: str


class UserResponse(BaseUser):
    """Public information about a user."""

    is_active: bool = True

    @classmethod
    def from_db_entry(cls, db_entry: User) -> Self:
        """From database entry."""
        return cls(**db_entry.model_dump(mode="python"))


class UserListResponse(SQLModel):
    """List of users."""

    users: list[UserResponse]

    @classmethod
    def from_db_entries(cls, db_entries: Sequence[User]) -> Self:
        """Create from database entries."""
        return cls(users=[UserResponse.from_db_entry(user) for user in db_entries])
