"""Test Song Database API lifespan."""

import unittest

from fastapi.testclient import TestClient
from songdb_server.api.app import create_app
from songdb_server.settings import SongDBSettings, SQLSettings
from sqlalchemy.exc import OperationalError


class TestSongDBApiLifespan(unittest.TestCase):
    """Test Song Database API lifespan."""

    def test_quit_on_db_failure(self) -> None:
        """Test immediately quitting on database connection failure."""
        for quit_on_failure in (False, True):
            with self.subTest(quit_on_failure=quit_on_failure):
                settings = SongDBSettings(
                    SQL=SQLSettings(
                        URL_OVERRIDE="mariadb+pymysql://nobody@nowhere:3306/db",
                        QUIT_ON_FAILURE=quit_on_failure,
                    )
                )
                app = create_app(settings)
                client = TestClient(app)
                if quit_on_failure:
                    self.assertRaises(OperationalError, client.__enter__)
                else:
                    client.__enter__()
                    client.__exit__()


if __name__ == "__main__":
    unittest.main()
