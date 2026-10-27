"""Test creating & modifying artists."""

import unittest

from fastapi import status
from songdb_server.models.artist import Artist, ArtistListResponse, ArtistPatchRequest
from songdb_server.models.user import UserResponse

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
        old_artist = self.validate_api_call(
            "get",
            f"/artists/{self.artist.uuid}",
            None,
            status.HTTP_200_OK,
            Artist,
        )
        old_user = self.validate_api_call(
            "get",
            "/users/me",
            None,
            status.HTTP_200_OK,
            UserResponse,
        )
        self.login()
        new_user = self.validate_api_call(
            "get",
            "/users/me",
            None,
            status.HTTP_200_OK,
            UserResponse,
        )
        self.assertNotEqual(old_user.uuid, new_user.uuid)

        new_name = self.fake.name()
        new_artist = self.validate_api_call(
            "patch",
            f"/artists/{self.artist.uuid}",
            ArtistPatchRequest(name=new_name),
            status.HTTP_200_OK,
            Artist,
        )

        self.assertEqual(new_artist.name, new_name)
        self.assertEqual(new_artist.creator_uuid, old_user.uuid)
        self.assertEqual(new_artist.created, old_artist.created)
        self.assertEqual(new_artist.modifier_uuid, new_user.uuid)
        self.assertGreater(new_artist.modified, old_artist.modified)


if __name__ == "__main__":
    unittest.main()
