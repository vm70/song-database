"""Test creating & modifying artists."""

import unittest

from fastapi import status
from songdb_server.models.artist import Artist, ArtistCreateRequest, ArtistListResponse

from test_common import AuthenticatedSongDBTestCase


class TestSongDBArtist(AuthenticatedSongDBTestCase):
    """Test creating & modifying artists."""

    artist: Artist

    def setUp(self):
        self.artist = self.validate_api_call(
            "post",
            "/artists",
            ArtistCreateRequest(name=self.faker.name()),
            status.HTTP_200_OK,
            Artist,
        )

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
        self.validate_api_call(
            "get",
            "/artists",
            None,
            status.HTTP_200_OK,
            ArtistListResponse,
        )


if __name__ == "__main__":
    unittest.main()
