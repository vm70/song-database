"""Songs API router."""

from fastapi.routing import APIRouter
from songdb_server.api.services.database import SessionDep
from songdb_server.models.song import Song, SongCreateRequest

songs_router = APIRouter(prefix="/songs", tags=["songs"])


@songs_router.post("")
def add_song(song_in: SongCreateRequest, session: SessionDep) -> Song:
    """Add a song."""
    song = Song.from_create_request(song_in)
    session.add(song)
    session.commit()
    session.refresh(song)
    return song
