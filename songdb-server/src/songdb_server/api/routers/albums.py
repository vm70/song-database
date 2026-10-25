"""Albums."""

from fastapi import HTTPException, status
from fastapi.routing import APIRouter
from songdb_server.api.services.database import SessionDep
from songdb_server.models.album import Album, AlbumCreateRequest
from songdb_server.models.album_artist import AlbumArtist
from songdb_server.models.artist import Artist

albums_router = APIRouter(prefix="/albums")


@albums_router.post("")
def add_album(album_in: AlbumCreateRequest, session: SessionDep) -> Album:
    """Add an album."""
    album = Album.from_create_request(album_in)

    for artist_uuid in album_in.artist_uuids:
        artist = session.get(Artist, artist_uuid)
        if artist is None:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not find artist with UUID {artist_uuid}",
            )
        session.add(
            AlbumArtist(
                album_uuid=album.uuid,
                artist_uuid=artist.uuid,
            )
        )

    session.add(album)
    session.commit()
    session.refresh(album)
    return album
