"""Database service."""

import logging
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import Engine
from sqlalchemy.exc import OperationalError
from sqlmodel import Session, SQLModel, create_engine

from songdb_server.settings import SongDBSettings

logger = logging.getLogger(__name__)


def init_engine(settings: SongDBSettings) -> Engine | None:
    """Initialize the SQLAlchemy engine."""
    try:
        engine = create_engine(
            url=settings.SQL.to_url(), connect_args=settings.SQL.CONNECT_ARGS
        )
        SQLModel.metadata.create_all(engine)
        return engine
    except OperationalError as e:
        logger.fatal(e)
        if settings.SQL.QUIT_ON_FAILURE:
            raise e
        return None


def get_session(request: Request) -> Generator[Session]:
    """Get the SQLAlchemy session."""
    if request.app.state.engine is None:
        raise HTTPException(
            status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not connect to SQL database",
        )

    with Session(request.app.state.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
