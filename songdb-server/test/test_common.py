"""Common utilities for unit tests."""

import unittest
from datetime import UTC, datetime, timedelta
from typing import Any

from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from songdb_server.api.app import app
from songdb_server.models.album import Album, AlbumCreateRequest
from songdb_server.models.artist import Artist, ArtistCreateRequest
from songdb_server.models.song import Song, SongCreateRequest
from songdb_server.models.token import Token
from songdb_server.models.user import UserCreateRequest
from sqlmodel import SQLModel


class SongDBTestCase(unittest.TestCase):
    """Song DB test case."""

    client: TestClient

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test case."""
        cls.client = TestClient(app)
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down the test case."""
        cls.client.__exit__()

    def validate_api_call[M: SQLModel](
        self,
        method: str,
        url: str,
        input_model: SQLModel | None,
        status_code: int,
        return_type: type[M],
        **kwargs: dict[str, Any],
    ) -> M:
        """Perform & validate an API call."""
        json = {} if input_model is None else input_model.model_dump(mode="json")
        # pyrefly: ignore[bad-argument-type]
        response = self.client.request(method=method, url=url, json=json, **kwargs)
        self.assertEqual(response.status_code, status_code, response.json())
        return return_type.model_validate(response.json())

    def run_api_call(
        self,
        method: str,
        url: str,
        input_model: SQLModel | None,
        status_code: int,
        **kwargs: dict[str, Any],
    ) -> None:
        """Perform an API call without return validation."""
        json = {} if input_model is None else input_model.model_dump(mode="json")
        # pyrefly: ignore[bad-argument-type]
        response = self.client.request(method=method, url=url, json=json, **kwargs)
        self.assertEqual(response.status_code, status_code, response.json())


class AuthenticatedSongDBTestCase(SongDBTestCase):
    """Test case with an authenticated client."""

    user: UserCreateRequest = UserCreateRequest(
        username="test-user", password="password"
    )
    token: Token
    faker: Faker

    @classmethod
    def login(cls):
        response = cls.client.post("/users", json=cls.user.model_dump(mode="json"))
        if response.status_code not in (status.HTTP_200_OK, status.HTTP_409_CONFLICT):
            msg = (
                f"Could not create test user {cls.user.username} for unit tests."
                + f"Error {response.status_code}: {response.json()}"
            )
            raise RuntimeError(msg)

        response = cls.client.post(
            "/users/token",
            data={
                "grant_type": "password",
                "username": cls.user.username,
                "password": cls.user.password,
            },
        )
        if response.status_code != status.HTTP_200_OK:
            msg = "Could not get token for testing"
            raise RuntimeError(msg)
        cls.token = Token.model_validate(response.json())
        cls.client.headers = {"Authorization": f"Bearer {cls.token.access_token}"}

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test case."""
        super().setUpClass()
        cls.login()
        cls.faker = Faker()

    def new_artist(self) -> Artist:
        return self.validate_api_call(
            "post",
            "/artists",
            ArtistCreateRequest(name=self.faker.name()),
            status.HTTP_200_OK,
            Artist,
        )

    def new_album(self, artist: Artist | None = None) -> Album:
        artist = artist or self.new_artist()
        return self.validate_api_call(
            "post",
            "/albums",
            AlbumCreateRequest(
                title=f"{artist.name}'s album",
                release_date=datetime.now(UTC),
                artist_uuids=[artist.uuid],
            ),
            status.HTTP_200_OK,
            Album,
        )

    def new_song(
        self, artist: Artist | None = None, album: Album | None = None
    ) -> Song:
        artist = artist or self.new_artist()
        album = album or self.new_album()
        return self.validate_api_call(
            "post",
            "/songs",
            SongCreateRequest(
                title=f"{artist.name}'s song",
                track_number=1,
                duration=timedelta(minutes=1),
                album_uuid=album.uuid,
            ),
            status.HTTP_200_OK,
            Song,
        )
