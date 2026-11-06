"""Key generation."""

import logging
import ssl
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateKey,
    EllipticCurvePublicKey,
)
from pydantic import SecretStr

logger = logging.getLogger(__name__)


def generate_es256_keys() -> tuple[SecretStr, SecretStr]:
    """Generate an ES256 key pair.

    Returns:
        tuple of PEM files: private key & public key
    """
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

    return (
        SecretStr(private_bytes.decode("utf8")),
        SecretStr(public_bytes.decode("utf8")),
    )


def verify_es256_keys(private_key: str, public_key: str) -> None:
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


def verify_https_certs(certfile: Path, keyfile: Path) -> None:
    """Verify a pair of HTTPS certificate files."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
