"""Test the Song database's OAuth2 service."""

import time
import unittest
from uuid import uuid4

from songdb_server.api.services.authentication import OAuth2Service
from songdb_server.api.services.database import init_engine
from songdb_server.models.user import User
from songdb_server.settings import SongDBSettings, default_sqlalchemy_url
from sqlalchemy import Engine


class TestSongDBOAuth2Service(unittest.TestCase):
    """Test the Song database's OAuth2 service."""

    service: OAuth2Service
    engine: Engine | None

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the class."""
        settings = SongDBSettings()
        settings.SQLALCHEMY_URL = default_sqlalchemy_url()
        cls.service = OAuth2Service(settings)
        cls.engine = init_engine(settings)

    def test_authenticate_user(self) -> None:
        """Test the time to fake user authentication."""
        test_user = User(
            uuid=uuid4(),
            username="example-user",
            hashed_password=self.service.get_password_hash("example-password"),
        )
        no_user = None

        times = []
        for user_input in (test_user, no_user):
            start = time.perf_counter()
            self.service.authenticate_user(user_input, password="example-password")
            stop = time.perf_counter()
            times.append(stop - start)

        self.assertAlmostEqual(times[0], times[1], delta=0.01)


if __name__ == "__main__":
    unittest.main()
