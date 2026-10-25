"""Artist models."""

from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from sqlmodel import SQLModel

from songdb_server.models._common import CreatedModifiedMixin, SongDBEntry


class BaseArtist(SQLModel):
    """Base artist class."""

    name: str


class ArtistCreateRequest(BaseArtist):
    """An artist creation request."""

    pass


class Artist(
    BaseArtist, CreatedModifiedMixin, SongDBEntry[ArtistCreateRequest], table=True
):
    """An artist in the song database."""

    @classmethod
    def from_create_request(
        cls, creator_uuid: UUID, create_request: ArtistCreateRequest
    ) -> Self:
        """Create an artist from an artist creation request."""
        creation_time = datetime.now(UTC)
        return cls(
            creator_uuid=creator_uuid,
            created=creation_time,
            modifier_uuid=creator_uuid,
            modified=creation_time,
            **create_request.model_dump(mode="python"),
        )


class ArtistListResponse(SQLModel):
    """A list of artists."""

    artists: list[Artist]
