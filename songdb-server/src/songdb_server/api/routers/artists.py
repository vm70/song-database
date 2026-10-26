"""Artists API router."""

from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from songdb_server.api.routers._common import get_item, get_items
from songdb_server.api.routers.users import (
    CurrentActiveUserDep,
    get_current_active_user,
)
from songdb_server.api.services.database import SessionDep
from songdb_server.models.artist import Artist, ArtistCreateRequest, ArtistListResponse

artists_router = APIRouter(prefix="/artists", tags=["artists"])


@artists_router.post("")
def add_artist(
    current_active_user: CurrentActiveUserDep,
    artist_in: ArtistCreateRequest,
    session: SessionDep,
) -> Artist:
    """Add an artist."""
    artist = Artist.from_create_request(current_active_user.uuid, artist_in)
    session.add(artist)
    session.commit()
    session.refresh(artist)
    return artist


@artists_router.get("/{artist_uuid}", dependencies=[Depends(get_current_active_user)])
def get_artist(
    artist_uuid: UUID,
    session: SessionDep,
) -> Artist:
    """Get an album."""
    return get_item(session, Artist, artist_uuid)


@artists_router.get("", dependencies=[Depends(get_current_active_user)])
def get_artists(
    session: SessionDep,
) -> ArtistListResponse:
    """Get all artists."""
    return ArtistListResponse(artists=get_items(session, Artist))
