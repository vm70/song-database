"""Album models."""

from datetime import datetime
from typing import Self
from uuid import UUID

from sqlmodel import SQLModel

from songdb_server.models._common import SongDBEntry


class BaseAlbum(SQLModel):
    """Base album class."""

    title: str
    release_date: datetime


class AlbumCreateRequest(BaseAlbum):
    """Album creation request."""

    artist_uuids: list[UUID]


class Album(BaseAlbum, SongDBEntry[AlbumCreateRequest], table=True):
    """Album entry in the song database."""

    @classmethod
    def from_create_request(cls, create_request: AlbumCreateRequest) -> Self:
        """Create an album from an album creation request."""
        return cls(**create_request.model_dump(mode="python"))
