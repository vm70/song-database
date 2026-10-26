"""Album models."""

from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from sqlmodel import SQLModel

from songdb_server.models._common import CreatedModifiedMixin, SongDBEntry


class BaseAlbum(SQLModel):
    """Base album class."""

    title: str
    release_date: datetime


class AlbumCreateRequest(BaseAlbum):
    """Album creation request."""

    artist_uuids: list[UUID]


class Album(
    BaseAlbum, CreatedModifiedMixin, SongDBEntry[AlbumCreateRequest], table=True
):
    """Album entry in the song database."""

    @classmethod
    def from_create_request(
        cls, creator_uuid: UUID, create_request: AlbumCreateRequest
    ) -> Self:
        """Create an album from an album creation request."""
        creation_time = datetime.now(UTC)
        return cls(
            creator_uuid=creator_uuid,
            created=creation_time,
            modifier_uuid=creator_uuid,
            modified=creation_time,
            **create_request.model_dump(mode="python"),
        )


class AlbumListResponse(SQLModel):
    """A list of artists."""

    albums: list[Album]
