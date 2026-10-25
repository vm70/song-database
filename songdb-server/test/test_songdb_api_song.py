"""Test creating & modifying songs."""

from datetime import UTC, datetime, timedelta

from fastapi import status
from songdb_server.models.album import Album, AlbumCreateRequest
from songdb_server.models.artist import Artist, ArtistCreateRequest
from songdb_server.models.song import Song, SongCreateRequest
from test_common import SongDBTestCase


class TestSongDBSong(SongDBTestCase):
    """Test creating & modifying songs."""

    def test_create_song(self) -> None:
        """Test creating a song."""
        artist = self.validate_api_call(
            "post",
            "/artists",
            ArtistCreateRequest(name="Test Artist 3"),
            status.HTTP_200_OK,
            Artist,
        )
        album = self.validate_api_call(
            "post",
            "/albums",
            AlbumCreateRequest(
                title="Test Artist 3's Album",
                release_date=datetime.now(tz=UTC),
                artist_uuids=[artist.uuid],
            ),
            status.HTTP_200_OK,
            Album,
        )
        self.validate_api_call(
            "post",
            "/songs",
            SongCreateRequest(
                track_number=1,
                title="Song in Test Artist 3's Album",
                duration=timedelta(minutes=3),
                album_uuid=album.uuid,
            ),
            status.HTTP_200_OK,
            Song,
        )
