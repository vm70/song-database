"""Test the Song database's OAuth2 service."""

import unittest

from songdb_server.api.services.authentication import OAuth2Service
from songdb_server.api.services.database import init_engine
from songdb_server.settings import SongDBSettings
from sqlalchemy import Engine


class TestSongDBOAuth2Service(unittest.TestCase):
    """Test the Song database's OAuth2 service."""

    service: OAuth2Service
    engine: Engine | None

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the class."""
        settings = SongDBSettings()
        cls.service = OAuth2Service(settings)
        cls.engine = init_engine(settings)

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down this class."""
        if cls.engine is not None:
            cls.engine.dispose()


if __name__ == "__main__":
    unittest.main()
