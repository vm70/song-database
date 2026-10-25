"""Artist models."""

from typing import Self

from sqlmodel import SQLModel

from songdb_server.models._common import SongDBEntry


class BaseArtist(SQLModel):
    """Base artist class."""

    name: str


class ArtistCreateRequest(BaseArtist):
    """An artist creation request."""

    pass


class Artist(BaseArtist, SongDBEntry[ArtistCreateRequest], table=True):
    """An artist in the song database."""

    @classmethod
    def from_create_request(cls, create_request: ArtistCreateRequest) -> Self:
        """Create an artist from an artist creation request."""
        return cls(**create_request.model_dump(mode="python"))


class ArtistListResponse(SQLModel):
    """A list of artists."""

    artists: list[Artist]
