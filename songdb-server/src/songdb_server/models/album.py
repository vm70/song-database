"""Album models."""

from datetime import datetime
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


class AlbumPatchRequest(SQLModel):
    """Album patch request."""

    pass


class Album(
    BaseAlbum,
    SongDBEntry[AlbumCreateRequest, AlbumPatchRequest],
    table=True,
):
    """Album entry in the song database."""

    pass


class AlbumListResponse(SQLModel):
    """A list of artists."""

    albums: list[Album]
