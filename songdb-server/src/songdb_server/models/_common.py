"""Common classes & mixins in the song database."""

from typing import Self
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class SongDBEntry[CR: SQLModel](SQLModel):
    """An entry in the song database."""

    uuid: UUID | None = Field(default_factory=uuid4, primary_key=True)
    """The UUID of the database entry."""

    @classmethod
    def from_create_request(cls, create_request: CR) -> Self:
        msg = "Not Implemented"
        raise NotImplementedError(msg)
