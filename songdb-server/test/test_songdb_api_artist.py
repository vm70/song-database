"""Test creating & modifying artists."""

import unittest

from fastapi import status
from songdb_server.models.artist import Artist, ArtistListResponse, ArtistPatchRequest

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

    def test_patch_artist(self) -> None:
        """Test modifying an artist."""
        new_name = self.faker.name()
        new_artist = self.validate_api_call(
            "patch",
            f"/artists/{self.artist.uuid}",
            ArtistPatchRequest(name=new_name),
            status.HTTP_200_OK,
            Artist,
        )
        self.assertEqual(new_artist.name, new_name)


if __name__ == "__main__":
    unittest.main()
