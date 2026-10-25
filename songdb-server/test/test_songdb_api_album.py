"""Test creating & modifying albums."""

import unittest
from datetime import UTC, datetime

from fastapi import status
from songdb_server.models.album import Album, AlbumCreateRequest
from songdb_server.models.artist import Artist, ArtistCreateRequest
from test_common import SongDBTestCase


class TestSongDBAlbum(SongDBTestCase):
    """Test creating & modifying albums."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.add_token_headers(cls)

    def test_create_album(self) -> None:
        """Test creating an album."""
        artist = self.validate_api_call(
            "post",
            "/artists",
            ArtistCreateRequest(name="Test Artist 2"),
            status.HTTP_200_OK,
            Artist,
        )
        self.validate_api_call(
            "post",
            "/albums",
            AlbumCreateRequest(
                title="Test Artist 2's Album",
                release_date=datetime.now(tz=UTC),
                artist_uuids=[artist.uuid],
            ),
            status.HTTP_200_OK,
            Album,
        )


if __name__ == "__main__":
    unittest.main()
