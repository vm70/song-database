"""Test core components of the SongDB API."""

import unittest

from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from songdb_server.api.app import create_app
from songdb_server.settings import ApiSettings, SongDBSettings

_settings = SongDBSettings()


class TestSongDBApiCore(unittest.TestCase):
    """Test core components of the SongDB API."""

    visible_app: FastAPI
    hidden_app: FastAPI

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the class with 2 clients."""
        cls.visible_app = create_app(
            SongDBSettings(
                API=ApiSettings(SHOW_DOCS=True, SHOW_REDOC=True, SHOW_OPENAPI_JSON=True)
            )
        )
        cls.hidden_app = create_app(
            SongDBSettings(
                API=ApiSettings(
                    SHOW_DOCS=False, SHOW_REDOC=False, SHOW_OPENAPI_JSON=False
                )
            )
        )

    def verify_visibility(self, url: str) -> None:
        """Verify whether a URL is visible based on settings."""
        for app, code in zip(
            (self.hidden_app, self.visible_app),
            (status.HTTP_404_NOT_FOUND, status.HTTP_200_OK),
            strict=True,
        ):
            with self.subTest(app=app, code=code), TestClient(app) as client:
                response = client.get(url)
                self.assertEqual(response.status_code, code)

    def test_docs(self) -> None:
        """Test loading Swagger documentation."""
        self.verify_visibility("/docs")

    def test_redoc(self) -> None:
        """Test loading Redoc documentation."""
        self.verify_visibility("/redoc")

    def test_openapi_json(self) -> None:
        """Test loading OpenAPI JSON documentation."""
        self.verify_visibility("/openapi.json")


if __name__ == "__main__":
    unittest.main()
