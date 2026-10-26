from collections.abc import Sequence
from uuid import UUID

from fastapi import HTTPException, status
from songdb_server.api.services.database import SessionDep
from sqlmodel import SQLModel, select


def get_item[I: SQLModel](
    session: SessionDep, item_type: type[I], item_uuid: UUID
) -> I:
    """Get an item from the SQL database.

    Args:
        session: SQLAlchemy Session
        item_type: SQLModel type
        item_uuid: UUID of the item of interest

    Returns:
        the item of interest

    Raises:
        HTTPException: 404 if the item isn't found
    """
    item = session.get(item_type, item_uuid)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find {item_type.__name__} with UUID {item_uuid}",
        )
    return item


def get_items[I: SQLModel](session: SessionDep, item_type: type[I]) -> Sequence[I]:
    """Get all items of a type from the SQL database.

    Args:
        session: SQLAlchemy Session
        item_type: SQLModel type

    Returns:
        A sequence of items
    """
    return session.exec(select(item_type)).all()
