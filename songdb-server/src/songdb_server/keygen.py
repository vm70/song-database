"""Key generation."""

# ruff: noqa: S603

import logging
import shutil
import subprocess

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateKey,
    EllipticCurvePublicKey,
)

logger = logging.getLogger(__name__)


def cryptography_hazmat_es256() -> tuple[str, str]:
    """Generate an ES256 key pair using `cryptography.hazmat`."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return private_bytes.decode("utf8"), public_bytes.decode("utf8")


def openssl_es256() -> tuple[str, str]:
    """Generate an ES256 key pair using OpenSSL."""
    openssl_path = shutil.which("openssl")
    if openssl_path is None:
        msg = "OpenSSL is not installed"
        raise FileNotFoundError(msg)
    private_key = subprocess.run(
        [
            openssl_path,
            "ecparam",
            "-name",
            "prime256v1",
            "-genkey",
            "-noout",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    public_key = subprocess.run(
        [
            openssl_path,
            "ec",
            "-pubout",
        ],
        check=True,
        capture_output=True,
        text=True,
        input=private_key,
    ).stdout
    return private_key, public_key


def generate_es256_key_pair() -> tuple[str, str]:
    """Generate an ES256 key pair."""
    try:
        return openssl_es256()
    except FileNotFoundError:
        logger.warning(
            "Could not find OpenSSL for key generation, "
            "Using cryptography.hazmat as fallback"
        )
    return cryptography_hazmat_es256()


def verify_keys(private_key: str, public_key: str) -> None:
    """Verify that a pair of keys for ES256 works.

    Raises:
        TypeError: if a key can't be converted into a cryptography object
        ValueError: if the keys don't match
    """
    private_key_obj = serialization.load_pem_private_key(
        private_key.encode("utf-8"), password=None
    )
    public_key_obj = serialization.load_pem_public_key(public_key.encode("utf-8"))
    if not isinstance(private_key_obj, EllipticCurvePrivateKey):
        msg = "Private key is not an elliptic curve private key"
        raise TypeError(msg)
    if not isinstance(public_key_obj, EllipticCurvePublicKey):
        msg = "Public key is not an elliptic curve public key"
        raise TypeError(msg)
    if private_key_obj.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ) != public_key_obj.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ):
        msg = "Public key & private key don't match"
        raise ValueError(msg)
