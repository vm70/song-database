"""Error model."""

from pydantic import BaseModel


class SongDBError(BaseModel):
    """Error class."""

    detail: str
