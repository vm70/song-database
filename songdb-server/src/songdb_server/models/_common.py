"""Common classes & mixins in the song database."""

from datetime import UTC, datetime
from typing import Self
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class SongDBEntry[C: SQLModel, R: SQLModel](SQLModel):
    """A non-user entry in the song database."""

    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    """The UUID of the database entry."""

    creator_uuid: UUID = Field(foreign_key="user.uuid")
    """UUID of who created the database entry."""
    created: datetime
    """Creation timestamp."""
    modifier_uuid: UUID = Field(foreign_key="user.uuid")
    """UUID of who last modified the database entry."""
    modified: datetime
    """Modification timestamp."""

    @classmethod
    def from_create_request(cls, create_request: C, creator_uuid: UUID) -> Self:
        """Create this entry from its corresponding creation request.

        Args:
            create_request: creation request
            creator_uuid: UUID of the user who created this object
        """
        creation_time = datetime.now(UTC)
        return cls(
            creator_uuid=creator_uuid,
            created=creation_time,
            modifier_uuid=creator_uuid,
            modified=creation_time,
            **create_request.model_dump(mode="python"),
        )

    def patch(self, patch_request: R, modifier_uuid: UUID) -> None:
        """Modify this class from a given patch request.

        Args:
            patch_request: corresponding patch request of this element
            modifier_uuid: UUID of the user who's patching this object
        """
        self.modified = datetime.now(UTC)
        self.modifier_uuid = modifier_uuid
        for key, value in patch_request.model_dump().items():
            setattr(self, key, value or getattr(self, key))
