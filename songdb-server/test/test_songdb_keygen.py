"""Key generation tests."""

import shutil
import unittest

from songdb_server.keygen import cryptography_hazmat_es256, openssl_es256, verify_keys

NO_OPENSSL = shutil.which("openssl") is None


class TestSongDBKeyGen(unittest.TestCase):
    """Test key generation."""

    @unittest.skipIf(NO_OPENSSL, "No OpenSSL implementation to generate keys")
    def test_openssl_es256(self) -> None:
        private_key_str, public_key_str = openssl_es256()
        verify_keys(private_key_str, public_key_str)

    def test_cryptography_es256(self) -> None:
        private_key_str, public_key_str = cryptography_hazmat_es256()
        verify_keys(private_key_str, public_key_str)


if __name__ == "__main__":
    unittest.main()
