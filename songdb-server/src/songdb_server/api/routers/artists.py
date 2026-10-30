"""Artists API router."""

from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from songdb_server.api.routers._common import get_item, get_items, patch_item
from songdb_server.api.routers.users import (
    CurrentActiveUserDep,
    get_current_active_user,
)
from songdb_server.api.services.database import SessionDep
from songdb_server.models.artist import (
    Artist,
    ArtistCreateRequest,
    ArtistListResponse,
    ArtistPatchRequest,
)

router = APIRouter(prefix="/artists", tags=["artists"])


@router.post("")
def add_artist(
    current_active_user: CurrentActiveUserDep,
    artist_in: ArtistCreateRequest,
    session: SessionDep,
) -> Artist:
    """Add an artist."""
    artist = Artist.from_create_request(artist_in, current_active_user.uuid)
    session.add(artist)
    session.commit()
    session.refresh(artist)
    return artist


@router.get("/{artist_uuid}", dependencies=[Depends(get_current_active_user)])
def get_artist(
    artist_uuid: UUID,
    session: SessionDep,
) -> Artist:
    """Get an album."""
    return get_item(session, Artist, artist_uuid)


@router.get("", dependencies=[Depends(get_current_active_user)])
def get_artists(
    session: SessionDep,
) -> ArtistListResponse:
    """Get all artists."""
    return ArtistListResponse(artists=get_items(session, Artist))


@router.patch("/{artist_uuid}")
def patch_artist(
    session: SessionDep,
    current_active_user: CurrentActiveUserDep,
    artist_uuid: UUID,
    artist_in: ArtistPatchRequest,
) -> Artist:
    """Modify an artist."""
    return patch_item(session, Artist, artist_uuid, artist_in, current_active_user.uuid)
