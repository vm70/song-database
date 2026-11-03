"""FastAPI application lifespan."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import Engine

from songdb_server.api.services.authentication import OAuth2Service
from songdb_server.api.services.database import init_engine
from songdb_server.settings import SongDBSettings


@asynccontextmanager
async def parameterized_lifespan(
    app: FastAPI, settings: SongDBSettings | None = None
) -> AsyncGenerator:
    """Parameterized FastAPI lifespan.

    Use this function as an input to `functools.partial` to apply a custom
    settings configuration.

    Args:
        app: FastAPI App
        settings: song database settings.

    Yields:
        None
    """
    app.state.settings = settings or SongDBSettings()
    app.state.oauth2_service = OAuth2Service(app.state.settings)
    app.state.engine = init_engine(app.state.settings)

    yield

    if isinstance(app.state.engine, Engine):
        app.state.engine.dispose()
