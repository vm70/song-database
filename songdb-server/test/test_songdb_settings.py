"""Test settings initialization."""

import unittest

from songdb_server.settings import SongDBSettings


class TestSongDBSettings(unittest.TestCase):
    """Test settings initialization."""

    def test_settings(self) -> None:
        """Test initializing settings."""
        settings = SongDBSettings()
        self.assertIsInstance(settings, SongDBSettings)


if __name__ == "__main__":
    unittest.main()
