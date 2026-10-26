"""Songs API router."""

from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from songdb_server.api.routers._common import get_item, get_items
from songdb_server.api.routers.users import (
    CurrentActiveUserDep,
    get_current_active_user,
)
from songdb_server.api.services.database import SessionDep
from songdb_server.models.album import Album
from songdb_server.models.song import Song, SongCreateRequest, SongListResponse

songs_router = APIRouter(prefix="/songs", tags=["songs"])


@songs_router.post("")
def add_song(
    current_active_user: CurrentActiveUserDep,
    song_in: SongCreateRequest,
    session: SessionDep,
) -> Song:
    """Add a song."""
    song = Song.from_create_request(song_in, current_active_user.uuid)
    session.add(song)
    session.commit()
    session.refresh(song)
    return song


@songs_router.get("/{song_uuid}")
def get_song(session: SessionDep, song_uuid: UUID) -> Song:
    """Get a song."""
    return get_item(session, Song, song_uuid)


@songs_router.get("/{song_uuid}/album")
def get_song_album(session: SessionDep, song_uuid: UUID) -> Album:
    """Get the album that this song belongs to."""
    song = get_item(session, Song, song_uuid)
    return get_item(session, Album, song.album_uuid)


@songs_router.get("", dependencies=[Depends(get_current_active_user)])
def get_songs(
    session: SessionDep,
) -> SongListResponse:
    """Get the list of all songs."""
    return SongListResponse(songs=get_items(session, Song))
