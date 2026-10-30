"""Artist models."""

from sqlmodel import Field, SQLModel

from songdb_server.models._common import SongDBEntry


class BaseArtist(SQLModel):
    """Base artist class."""

    name: str = Field(min_length=1)


class ArtistCreateRequest(BaseArtist):
    """An artist creation request."""

    pass


class ArtistPatchRequest(SQLModel):
    """Artist patch request."""

    name: str | None = Field(min_length=1)


class Artist(
    BaseArtist,
    SongDBEntry[ArtistCreateRequest, ArtistPatchRequest],
    table=True,
):
    """An artist in the song database."""


class ArtistListResponse(SQLModel):
    """A list of artists."""

    artists: list[Artist]
