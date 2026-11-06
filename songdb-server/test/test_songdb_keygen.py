"""Key generation tests."""

import unittest

from songdb_server.keygen import generate_es256_keys, verify_es256_keys


class TestSongDBKeyGen(unittest.TestCase):
    """Test key generation."""

    def test_generate_es256_keys(self) -> None:
        """Test generating ES256 key pairs."""
        private_key, public_key = generate_es256_keys()
        verify_es256_keys(private_key.get_secret_value(), public_key.get_secret_value())

    def test_es256_key_mismatch(self) -> None:
        """Test that mismatched ES256 key pairs throw an error."""
        private_key_1, public_key_1 = generate_es256_keys()
        private_key_2, public_key_2 = generate_es256_keys()
        self.assertRaises(
            ValueError,
            verify_es256_keys,
            private_key_1.get_secret_value(),
            public_key_2.get_secret_value(),
        )
        self.assertRaises(
            ValueError,
            verify_es256_keys,
            private_key_2.get_secret_value(),
            public_key_1.get_secret_value(),
        )


if __name__ == "__main__":
    unittest.main()
