"""FastAPI application."""

import json
from importlib.metadata import metadata
from os import PathLike

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from songdb_server.api.lifespan import lifespan
from songdb_server.api.routers import albums, artists, songs, users
from songdb_server.settings import env_settings

_settings = env_settings()

app = FastAPI(
    title="Song Database API",
    version=metadata("songdb-server")["Version"],
    lifespan=lifespan,
    openapi_url="/openapi.json" if _settings.API.SHOW_OPENAPI_JSON else None,
    docs_url="/docs" if _settings.API.SHOW_DOCS else None,
    redoc_url="/redoc" if _settings.API.SHOW_REDOC else None,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(albums.router)
app.include_router(artists.router)
app.include_router(songs.router)
app.include_router(users.router)


def export_openapi_json(path: PathLike) -> None:
    """Export the song database's OpenAPI JSON specification."""
    openapi_schema = app.openapi()
    with open(path, "w") as f:  # noqa: PTH123
        json.dump(openapi_schema, f, indent=4)
