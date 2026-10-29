"""Test settings initialization."""

import os
import secrets
import unittest

from songdb_server.settings import SongDBSettings


class TestSongDBSettings(unittest.TestCase):
    """Test settings initialization."""

    def test_settings(self) -> None:
        """Test initializing settings."""
        os.environ["SONGDB__SQL__PASSWORD"] = secrets.token_urlsafe(16)
        os.environ["SONGDB__AUTH__JWT_SECRET"] = secrets.token_hex(64)
        settings = SongDBSettings()
        self.assertIsInstance(settings, SongDBSettings)


if __name__ == "__main__":
    unittest.main()
