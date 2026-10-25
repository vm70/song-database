"""Test creating & modifying artists."""

import unittest

from fastapi import status
from songdb_server.models.artist import Artist, ArtistCreateRequest
from test_common import SongDBTestCase


class TestSongDBArtist(SongDBTestCase):
    """Test creating & modifying artists."""

    def test_create_artist(self) -> None:
        """Test creating an artist."""
        self.validate_api_call(
            "post",
            "/artists",
            ArtistCreateRequest(name="Test artist 1"),
            status.HTTP_200_OK,
            Artist,
        )


if __name__ == "__main__":
    unittest.main()
