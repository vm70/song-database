"""Artist models."""

from sqlmodel import SQLModel

from songdb_server.models._common import SongDBEntry


class BaseArtist(SQLModel):
    """Base artist class."""

    name: str


class ArtistCreateRequest(BaseArtist):
    """An artist creation request."""

    pass


class ArtistPatchRequest(SQLModel):
    """Artist patch request."""

    name: str | None = None


class Artist(
    BaseArtist,
    SongDBEntry[ArtistCreateRequest, ArtistPatchRequest],
    table=True,
):
    """An artist in the song database."""


class ArtistListResponse(SQLModel):
    """A list of artists."""

    artists: list[Artist]
