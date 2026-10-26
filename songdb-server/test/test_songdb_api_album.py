"""Test creating & modifying albums."""

import unittest

from fastapi import status
from songdb_server.models.album import Album, AlbumListResponse
from songdb_server.models.artist import Artist

from test_common import AuthenticatedSongDBTestCase


class TestSongDBAlbum(AuthenticatedSongDBTestCase):
    """Test creating & modifying albums."""

    artist: Artist
    album: Album

    def setUp(self) -> None:
        self.artist = self.new_artist()
        self.album = self.new_album(self.artist)

    def test_get_album(self) -> None:
        """Test fetching an album."""
        self.validate_api_call(
            "get",
            f"/albums/{self.album.uuid}",
            None,
            status.HTTP_200_OK,
            Album,
        )

    def test_get_albums(self) -> None:
        """Test fetching all albums."""
        self.validate_api_call(
            "get",
            "/albums",
            None,
            status.HTTP_200_OK,
            AlbumListResponse,
        )


if __name__ == "__main__":
    unittest.main()
