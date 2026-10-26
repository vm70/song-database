"""FastAPI application."""

import json
from importlib.metadata import metadata
from os import PathLike

from fastapi import FastAPI

from songdb_server.api.lifespan import lifespan
from songdb_server.api.routers.albums import albums_router
from songdb_server.api.routers.artists import artists_router
from songdb_server.api.routers.songs import songs_router
from songdb_server.api.routers.users import users_router

app = FastAPI(
    title="Song Database API",
    version=metadata("songdb-server")["Version"],
    lifespan=lifespan,
)

app.include_router(songs_router)
app.include_router(albums_router)
app.include_router(artists_router)
app.include_router(users_router)


def export_openapi_json(path: PathLike) -> None:
    """Export the song database's OpenAPI JSON specification."""
    openapi_schema = app.openapi()
    with open(path, "w") as f:  # noqa: PTH123
        json.dump(openapi_schema, f, indent=4)
