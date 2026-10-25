"""Artists API router."""

from fastapi.routing import APIRouter
from songdb_server.api.services.database import SessionDep
from songdb_server.models.artist import Artist, ArtistCreateRequest, ArtistListResponse
from sqlmodel import select

artists_router = APIRouter(prefix="/artists", tags=["artists"])


@artists_router.post("")
def add_artist(artist_in: ArtistCreateRequest, session: SessionDep) -> Artist:
    """Add an artist."""
    artist = Artist.from_create_request(artist_in)
    session.add(artist)
    session.commit()
    session.refresh(artist)
    return artist


@artists_router.get("")
def get_artists(
    session: SessionDep,
) -> ArtistListResponse:
    """Get all artists."""
    return ArtistListResponse(artists=session.exec(select(Artist)).all())
