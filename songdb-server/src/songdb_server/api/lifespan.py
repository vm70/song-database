"""FastAPI application lifespan."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import Engine

from songdb_server.api.services.authentication import OAuth2Service
from songdb_server.api.services.database import init_engine
from songdb_server.settings import SongDBSettings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """FastAPI application lifespan."""
    app.state.settings = SongDBSettings()
    app.state.oauth2_service = OAuth2Service(app.state.settings)
    app.state.engine = init_engine(app.state.settings)

    yield

    if isinstance(app.state.engine, Engine):
        app.state.engine.dispose()
