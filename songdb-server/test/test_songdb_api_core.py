"""Test core components of the SongDB API."""

import unittest

from fastapi import status
from songdb_server.settings import SongDBSettings

from test_common import SongDBTestCase

_settings = SongDBSettings()


class TestSongDBApiCore(SongDBTestCase):
    """Test core components of the SongDB API."""

    @unittest.skipIf(not _settings.API.SHOW_DOCS, reason="Docs endpoint is disabled")
    def test_docs(self) -> None:
        """Test loading Swagger documentation."""
        response = self.client.get("/docs")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @unittest.skipIf(not _settings.API.SHOW_REDOC, reason="Redoc endpoint is disabled")
    def test_redoc(self) -> None:
        """Test getting the Redoc specification."""
        response = self.client.get("/redoc")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @unittest.skipIf(
        not _settings.API.SHOW_OPENAPI_JSON, reason="OpenAPI JSON is disabled"
    )
    def test_openapi_json(self) -> None:
        """Test getting the OpenAPI JSON specification."""
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
