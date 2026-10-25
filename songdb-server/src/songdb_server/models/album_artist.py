"""Junction table mapping albums and artists."""

from uuid import UUID

from sqlmodel import Field, SQLModel

from songdb_server.models._common import SongDBEntry


class BaseAlbumArtist(SQLModel):
    """Base Album-artist junction class."""

    album_uuid: UUID | None = Field(foreign_key="album.uuid")
    artist_uuid: UUID | None = Field(foreign_key="artist.uuid")


class AlbumArtist(BaseAlbumArtist, SongDBEntry, table=True):
    """Junction element mapping artists to albums."""

    pass
