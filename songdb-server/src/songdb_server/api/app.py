"""FastAPI application."""

import json
from functools import partial
from importlib.metadata import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from songdb_server.api.lifespan import parameterized_lifespan
from songdb_server.api.routers import albums, artists, songs, users
from songdb_server.settings import SongDBSettings


def create_app(settings: SongDBSettings | None = None) -> FastAPI:
    """Create a new Song Database server application.

    This is the factory function for the Song Database API server.

    Args:
        settings:
            API settings. If none provided, settings are inferred from
            environment variables.
    """
    settings = settings or SongDBSettings()

    app = FastAPI(
        title="Song Database API",
        version=metadata("songdb-server")["Version"],
        lifespan=partial(parameterized_lifespan, settings=settings),
        openapi_url="/openapi.json" if settings.API.SHOW_OPENAPI_JSON else None,
        docs_url="/docs" if settings.API.SHOW_DOCS else None,
        redoc_url="/redoc" if settings.API.SHOW_REDOC else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://localhost:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(HTTPSRedirectMiddleware)

    app.include_router(albums.router)
    app.include_router(artists.router)
    app.include_router(songs.router)
    app.include_router(users.router)

    return app


def export_openapi_json(path: Path) -> None:
    """Export the song database's OpenAPI JSON specification."""
    app = create_app()
    openapi_schema = app.openapi()
    with path.open("w") as f:
        json.dump(openapi_schema, f, indent=4)
