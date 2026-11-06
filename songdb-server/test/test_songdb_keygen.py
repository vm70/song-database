"""Key generation tests."""

import shutil
import unittest

from songdb_server.keygen import generate_es256_keys, verify_keys

NO_OPENSSL = shutil.which("openssl") is None


class TestSongDBKeyGen(unittest.TestCase):
    """Test key generation."""

    def test_generate_es256_keys(self) -> None:
        """Test generating ES256 key pairs."""
        private_key_str, public_key_str = generate_es256_keys()
        verify_keys(
            private_key_str.get_secret_value(), public_key_str.get_secret_value()
        )


if __name__ == "__main__":
    unittest.main()
