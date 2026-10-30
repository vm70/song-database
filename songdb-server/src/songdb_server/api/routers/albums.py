"""Albums."""

from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from songdb_server.api.routers._common import get_item, get_items
from songdb_server.api.routers.users import (
    CurrentActiveUserDep,
    get_current_active_user,
)
from songdb_server.api.services.database import SessionDep
from songdb_server.models.album import Album, AlbumCreateRequest, AlbumListResponse
from songdb_server.models.album_artist import AlbumArtist
from songdb_server.models.artist import Artist

router = APIRouter(prefix="/albums", tags=["albums"])


@router.post("")
def add_album(
    current_active_user: CurrentActiveUserDep,
    album_in: AlbumCreateRequest,
    session: SessionDep,
) -> Album:
    """Add an album."""
    album = Album.from_create_request(album_in, current_active_user.uuid)

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
                creator_uuid=album.creator_uuid,
                created=album.created,
                modifier_uuid=album.modifier_uuid,
                modified=album.modified,
                album_uuid=album.uuid,
                artist_uuid=artist_uuid,
            )
        )

    session.add(album)
    session.commit()
    session.refresh(album)
    return album


@router.get("/{album_uuid}", dependencies=[Depends(get_current_active_user)])
def get_album(
    album_uuid: UUID,
    session: SessionDep,
) -> Album:
    """Get an album."""
    return get_item(session, Album, album_uuid)


@router.get("", dependencies=[Depends(get_current_active_user)])
def get_albums(
    session: SessionDep,
) -> AlbumListResponse:
    """Get all albums."""
    return AlbumListResponse(albums=get_items(session, Album))
