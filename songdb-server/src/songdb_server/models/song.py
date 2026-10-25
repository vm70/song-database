"""Song models."""

from datetime import timedelta
from typing import Self
from uuid import UUID

from pydantic import NonNegativeInt
from sqlmodel import Field, SQLModel

from songdb_server.models._common import SongDBEntry


class BaseSong(SQLModel):
    """Base song class."""

    title: str
    track_number: NonNegativeInt
    duration: timedelta
    album_uuid: UUID = Field(foreign_key="album.uuid")


class SongCreateRequest(BaseSong):
    """Song creation request."""

    pass


class Song(BaseSong, SongDBEntry[SongCreateRequest], table=True):
    """Song entry in the database."""

    @classmethod
    def from_create_request(cls, create_request: SongCreateRequest) -> Self:
        """Create a song entry from a song creation request."""
        return cls(**create_request.model_dump(mode="python"))
