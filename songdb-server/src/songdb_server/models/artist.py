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


class ArtistPatchRequest(SQLModel):
    """Artist patch request."""

    name: str | None = None


class Artist(
    BaseArtist,
    CreatedModifiedMixin,
    SongDBEntry[ArtistCreateRequest, ArtistPatchRequest],
    table=True,
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

    def patch(self, patcher_uuid: UUID, patch_request: ArtistPatchRequest) -> None:
        """Modify this class from a given patch request.

        Args:
            patcher_uuid: UUID of the user who's patching this object
            patch_request: corresponding patch request of this element
        """
        if not isinstance(patch_request, ArtistPatchRequest):
            msg = f"Invalid type for patch request: {type(patch_request)}"
            raise TypeError(msg)
        super().patch(patcher_uuid, patch_request)


class ArtistListResponse(SQLModel):
    """A list of artists."""

    artists: list[Artist]
