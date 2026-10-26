"""Common classes & mixins in the song database."""

from datetime import datetime
from typing import Self
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class SongDBEntry[CR: SQLModel](SQLModel):
    """An entry in the song database."""

    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    """The UUID of the database entry."""

    @classmethod
    def from_create_request(cls, creator_uuid: UUID, create_request: CR) -> Self:
        """Create an entry from its corresponding creation request.

        Args:
            creator_uuid: UUID of the user who created this object
            create_request: corresponding creation request of this element
        """
        msg = "Not Implemented"
        raise NotImplementedError(msg)

    def patch(self, patch_request: SQLModel) -> None:
        """Modify this class from a given patch request."""
        for key, value in patch_request.model_dump().items():
            setattr(self, key, value or getattr(self, key))


class CreatedModifiedMixin(SQLModel):
    """Mixin class for storing who created or last modified an entry."""

    creator_uuid: UUID = Field(foreign_key="user.uuid")
    """UUID of who created the database entry."""
    created: datetime
    """Creation timestamp."""
    modifier_uuid: UUID = Field(foreign_key="user.uuid")
    """UUID of who last modified the database entry."""
    modified: datetime
    """Modification timestamp."""
