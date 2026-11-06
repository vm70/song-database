"""Test settings initialization."""

import unittest

from pydantic import SecretStr
from songdb_server.settings import AuthSettings, SongDBSettings, SQLSettings


class TestSongDBSettings(unittest.TestCase):
    """Test settings initialization."""

    def test_settings(self) -> None:
        """Test initializing settings."""
        settings = SongDBSettings()
        self.assertIsInstance(settings, SongDBSettings)

    def test_auth_settings_no_jwt(self) -> None:
        """Test that authentication won't break if no JWT keys are provided."""
        auth_settings = AuthSettings(
            JWT_PRIVATE_KEY=None,
            JWT_PRIVATE_KEY_FILE=None,
            JWT_PUBLIC_KEY=None,
            JWT_PUBLIC_KEY_FILE=None,
        )
        self.assertIsInstance(auth_settings.JWT_PUBLIC_KEY, SecretStr)
        self.assertIsInstance(auth_settings.JWT_PRIVATE_KEY, SecretStr)

    def test_settings_url_override(self) -> None:
        """Test URL override settings."""
        shared_settings = {
            "DRIVERNAME": "mariadb+pymysql",
            "USERNAME": "user",
            "PASSWORD": "password",
            "HOST": "mariadb",
            "PORT": 3306,
            "DATABASE": "db",
        }
        sql_settings = SQLSettings(
            **shared_settings,
            URL_OVERRIDE="sqlite:///database.db",
        )
        for key, val in shared_settings.items():
            with self.subTest(key=key, val=val):
                self.assertNotEqual(getattr(sql_settings, key), val)


if __name__ == "__main__":
    unittest.main()
