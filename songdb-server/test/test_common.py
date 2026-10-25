"""Common utilities for unit tests."""

import os
import unittest
from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from songdb_server.api.app import app
from songdb_server.models.token import Token
from songdb_server.models.user import UserCreateRequest, UserResponse
from sqlmodel import SQLModel


class SongDBTestCase(unittest.TestCase):
    """Song DB test case."""

    client: TestClient

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test case."""
        os.environ["SONGDB__SQLALCHEMY_URL"] = (
            "sqlite:///file:memdb1?mode=memory&cache=shared&uri=true"
        )
        cls.client = TestClient(app)
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down the test case."""
        cls.client.__exit__()

    def validate_api_call[T: SQLModel](
        self,
        method: str,
        url: str,
        input_model: SQLModel | None,
        status_code: int,
        return_type: type[T] | None,
        **kwargs: dict[str, Any],
    ) -> T:
        """Perform & validate an API call."""
        json = {} if input_model is None else input_model.model_dump(mode="json")
        response = self.client.request(method=method, url=url, json=json, **kwargs)
        self.assertEqual(response.status_code, status_code, response.json())
        if return_type is not None:
            return return_type.model_validate(response.json())
        return None


class AuthenticatedSongDBTestCase(SongDBTestCase):
    """Test case with an authenticated client."""

    token: Token

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test case."""
        super().setUpClass()

        response = cls.client.post(
            "/users",
            json=UserCreateRequest(
                username="test-user", password="password"
            ).model_dump(mode="json"),
        )
        if response.status_code != status.HTTP_200_OK:
            msg = "Could not create user for testing"
            raise RuntimeError(msg)
        UserResponse.model_validate(response.json())

        response = cls.client.post(
            "/users/token",
            data={
                "grant_type": "password",
                "username": "test-user",
                "password": "password",
            },
        )
        if response.status_code != status.HTTP_200_OK:
            msg = "Could not get token for testing"
            raise RuntimeError(msg)
        cls.token = Token.model_validate(response.json())

        cls.client.headers = {"Authorization": f"Bearer {cls.token.access_token}"}
