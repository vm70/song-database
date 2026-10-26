"""Song models."""

from datetime import UTC, datetime, timedelta
from typing import Self
from uuid import UUID

from pydantic import NonNegativeInt
from sqlmodel import Field, SQLModel

from songdb_server.models._common import CreatedModifiedMixin, SongDBEntry


class BaseSong(SQLModel):
    """Base song class."""

    title: str
    track_number: NonNegativeInt
    duration: timedelta
    album_uuid: UUID = Field(foreign_key="album.uuid")


class SongCreateRequest(BaseSong):
    """Song creation request."""

    pass


class Song(BaseSong, CreatedModifiedMixin, SongDBEntry[SongCreateRequest], table=True):
    """Song entry in the database."""

    @classmethod
    def from_create_request(
        cls, creator_uuid: UUID, create_request: SongCreateRequest
    ) -> Self:
        """Create a song entry from a song creation request."""
        creation_time = datetime.now(UTC)
        return cls(
            creator_uuid=creator_uuid,
            created=creation_time,
            modifier_uuid=creator_uuid,
            modified=creation_time,
            **create_request.model_dump(mode="python"),
        )


class SongListResponse(SQLModel):
    """A list of songs."""

    songs: list[Song]
