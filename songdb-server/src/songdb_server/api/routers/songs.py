"""Songs API router."""

from fastapi import Depends
from fastapi.routing import APIRouter
from songdb_server.api.routers.users import (
    CurrentActiveUserDep,
    get_current_active_user,
)
from songdb_server.api.services.database import SessionDep
from songdb_server.models.song import Song, SongCreateRequest, SongListResponse
from sqlmodel import select

songs_router = APIRouter(prefix="/songs", tags=["songs"])


@songs_router.post("")
def add_song(
    current_active_user: CurrentActiveUserDep,
    song_in: SongCreateRequest,
    session: SessionDep,
) -> Song:
    """Add a song."""
    song = Song.from_create_request(current_active_user.uuid, song_in)
    session.add(song)
    session.commit()
    session.refresh(song)
    return song


@songs_router.get("", dependencies=[Depends(get_current_active_user)])
def get_songs(
    session: SessionDep,
) -> SongListResponse:
    """Get the list of all songs."""
    return SongListResponse(songs=session.exec(select(Song)).all())
