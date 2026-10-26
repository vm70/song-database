"""Song models."""

from datetime import timedelta
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


class SongPatchRequest(SQLModel):
    """Song patch request."""

    pass


class Song(
    BaseSong,
    SongDBEntry[SongCreateRequest, SongPatchRequest],
    table=True,
):
    """Song entry in the database."""


class SongListResponse(SQLModel):
    """A list of songs."""

    songs: list[Song]
