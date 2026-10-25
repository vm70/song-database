"""Test user settings with the SongDB API."""
# ruff: noqa: S106

import unittest

from fastapi import status
from songdb_server.models.token import Token
from songdb_server.models.user import UserCreateRequest, UserResponse
from test_common import SongDBTestCase


class TestSongDBUser(SongDBTestCase):
    """Test user settings with the SongDB API."""

    def test_create_user(self) -> None:
        """Test creating & authenticating a user."""
        self.validate_api_call(
            "post",
            "/users",
            UserCreateRequest(username="test-user", password="password"),
            status.HTTP_200_OK,
            UserResponse,
        )
        response = self.client.post(
            "/users/token",
            data={
                "grant_type": "password",
                "username": "test-user",
                "password": "password",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        token = Token.model_validate(response.json())
        self.validate_api_call(
            "get",
            "/users/me",
            None,
            status.HTTP_200_OK,
            UserResponse,
            headers={"Authorization": f"Bearer {token.access_token}"},
        )
        self.validate_api_call(
            "delete",
            "/users/me",
            None,
            status.HTTP_200_OK,
            None,
            headers={"Authorization": f"Bearer {token.access_token}"},
        )
        self.validate_api_call(
            "get",
            "/users/me",
            None,
            status.HTTP_401_UNAUTHORIZED,
            None,
            headers={"Authorization": f"Bearer {token.access_token}"},
        )

    def test_create_same_username(self) -> None:
        """Test creating 2 users with the same username won't work."""
        self.validate_api_call(
            "post",
            "/users",
            UserCreateRequest(username="duplicate-user", password="duplicate-password"),
            status.HTTP_200_OK,
            UserResponse,
        )
        self.validate_api_call(
            "post",
            "/users",
            UserCreateRequest(username="duplicate-user", password="duplicate-password"),
            status.HTTP_409_CONFLICT,
            None,
        )


if __name__ == "__main__":
    unittest.main()
