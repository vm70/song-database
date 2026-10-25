"""Songs API router."""

from fastapi.routing import APIRouter
from songdb_server.api.routers.users import CurrentActiveUserDep
from songdb_server.api.services.database import SessionDep
from songdb_server.models.song import Song, SongCreateRequest

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
