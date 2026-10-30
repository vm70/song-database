"""Key generation."""

# ruff: noqa: S603

import logging
import shutil
import subprocess

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

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
