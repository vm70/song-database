"""Test creating & modifying songs."""

import unittest

from fastapi import status
from songdb_server.models.album import Album
from songdb_server.models.artist import Artist
from songdb_server.models.song import Song, SongListResponse

from test_common import AuthenticatedSongDBTestCase


class TestSongDBSong(AuthenticatedSongDBTestCase):
    """Test creating & modifying songs."""

    artist: Artist
    album: Album
    song: Song

    def setUp(self) -> None:
        self.artist = self.new_artist()
        self.album = self.new_album(self.artist)
        self.song = self.new_song(self.artist, self.album)

    def test_get_song(self) -> None:
        """Test fetching a song."""
        self.validate_api_call(
            "get",
            f"/songs/{self.song.uuid}",
            None,
            status.HTTP_200_OK,
            Song,
        )

    def test_get_songs(self) -> None:
        """Test fetching all songs."""
        self.validate_api_call(
            "get",
            "/songs",
            None,
            status.HTTP_200_OK,
            SongListResponse,
        )


if __name__ == "__main__":
    unittest.main()
