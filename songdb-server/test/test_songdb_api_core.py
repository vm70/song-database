"""Test core components of the SongDB API."""

import unittest

from fastapi import status
from test_common import SongDBTestCase


class TestSongDBApiCore(SongDBTestCase):
    """Test core components of the SongDB API."""

    def test_docs(self) -> None:
        """Test loading Swagger documentation."""
        response = self.client.get("/docs")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_openapi_json(self) -> None:
        """Test getting the OpenAPI JSON specification."""
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
