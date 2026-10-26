"""Test creating & modifying artists."""

import unittest

from fastapi import status
from songdb_server.models.artist import Artist, ArtistListResponse

from test_common import AuthenticatedSongDBTestCase


class TestSongDBArtist(AuthenticatedSongDBTestCase):
    """Test creating & modifying artists."""

    artist: Artist

    def setUp(self) -> None:
        self.artist = self.new_artist()

    def test_get_artist(self) -> None:
        """Test fetching an artist."""
        self.validate_api_call(
            "get",
            f"/artists/{self.artist.uuid}",
            None,
            status.HTTP_200_OK,
            Artist,
        )

    def test_get_artists(self) -> None:
        """Test fetching all artists."""
        self.validate_api_call(
            "get",
            "/artists",
            None,
            status.HTTP_200_OK,
            ArtistListResponse,
        )


if __name__ == "__main__":
    unittest.main()
