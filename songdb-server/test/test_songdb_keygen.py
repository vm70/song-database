"""Key generation tests."""

import shutil
import unittest

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateKey,
    EllipticCurvePublicKey,
)
from songdb_server.keygen import cryptography_hazmat_es256, openssl_es256

NO_OPENSSL = shutil.which("openssl") is None


class TestSongDBKeyGen(unittest.TestCase):
    """Test key generation."""

    def instantiate_keys(self, private_key_str: str, public_key_str: str):
        private_key = serialization.load_pem_private_key(
            private_key_str.encode("utf-8"), password=None
        )
        public_key = serialization.load_pem_public_key(public_key_str.encode("utf-8"))
        self.assertIsInstance(private_key, EllipticCurvePrivateKey)
        self.assertIsInstance(public_key, EllipticCurvePublicKey)
        self.assertEqual(
            private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ),
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ),
        )

    @unittest.skipIf(NO_OPENSSL, "No OpenSSL implementation to generate keys")
    def test_openssl_es256(self) -> None:
        private_key_str, public_key_str = openssl_es256()
        self.instantiate_keys(private_key_str, public_key_str)

    def test_cryptography_es256(self) -> None:
        private_key_str, public_key_str = cryptography_hazmat_es256()
        self.instantiate_keys(private_key_str, public_key_str)


if __name__ == "__main__":
    unittest.main()
