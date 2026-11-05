#!/usr/bin/env python3
"""Generate example secrets for the song database.

Usage:
    ```bash
    uv run scripts/generate_secrets.py
    ```
"""

import argparse
import logging
import secrets
import string
from datetime import UTC, datetime, timedelta
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.x509.oid import NameOID


def setup_secret_file(secret_file: Path) -> None:
    """Set up a secret file for writing."""
    if secret_file.exists() and secret_file.is_dir():
        msg = f"Path {secret_file} is a directory"
        raise IsADirectoryError(msg)
    secret_file.parent.mkdir(parents=True, exist_ok=True)


def generate_password(
    password_file: Path, length: int = 20, *, overwrite: bool = False
) -> None:
    """Generate a password with a specified length and save it to the given path.

    Args:
        password_file: File path to where the password will be stored.
        length: length of the password in characters.
        overwrite: whether to overwrite the file if it already exists.

    See Also:
        https://docs.python.org/3/library/secrets.html
    """
    setup_secret_file(password_file)
    if overwrite is False and password_file.exists():
        print(f"Password file {password_file} already exists")
        return
    print(f"Writing password file to {password_file}")

    password = "".join(
        [
            secrets.choice(string.ascii_letters + string.digits + string.punctuation)
            for _ in range(length)
        ]
    )
    password_file.parent.mkdir(parents=True, exist_ok=True)
    password_file.write_text(password)


def generate_es256_key_pair(
    private_key_file: Path, public_key_file: Path, *, overwrite: bool = False
) -> None:
    """Generate an ES256 key pair and save them to the given paths.

    Args:
        private_key_file: File path to where the private key will be stored.
        public_key_file: File path to where the public key will be stored.
        overwrite: whether to overwrite the files if they already exists.
    """
    setup_secret_file(private_key_file)
    setup_secret_file(public_key_file)
    if overwrite is False and private_key_file.exists() and public_key_file.exists():
        print(f"ES256 key pair {private_key_file} & {public_key_file} already exist")
        return
    print(f"Writing ES256 key pair {private_key_file} & {public_key_file}")

    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    private_key_file.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    public_key_file.write_bytes(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )


def generate_self_signed_cert(
    private_key_file: Path, cert_key_file: Path, *, overwrite: bool = False
) -> None:
    """Generate a self-signed certificate.

    Args:
        private_key_file: File path to where the private key will be stored.
        cert_key_file: File path to where the certification will be stored.
        overwrite: whether to overwrite the files if they already exist.

    See Also:
        https://cryptography.io/en/latest/x509/tutorial/#creating-a-self-signed-certificate
    """
    setup_secret_file(private_key_file)
    setup_secret_file(cert_key_file)
    if overwrite is False and private_key_file.exists() and cert_key_file.exists():
        print(
            "Private key & certificate",
            f"{private_key_file}, {cert_key_file}",
            "already exist",
            sep=" ",
        )
        return
    print(f"Writing private key & certificate {private_key_file}, {cert_key_file}")

    issuing_time = datetime.now(UTC)
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key_file.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "XX"),
        ]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(issuing_time)
        .not_valid_after(issuing_time + timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False
        )
    ).sign(private_key, hashes.SHA256())

    cert_key_file.write_bytes(cert.public_bytes(serialization.Encoding.PEM))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--overwrite", action="store_true")
    parser.add_argument(
        "--mariadb-password-file",
        type=Path,
        default=Path("./secrets/songdb-mariadb-password"),
    )
    parser.add_argument(
        "--mariadb-root-password-file",
        type=Path,
        default=Path("./secrets/songdb-mariadb-root-password"),
    )
    parser.add_argument(
        "--jwt-private-key-file",
        type=Path,
        default=Path("./secrets/songdb-auth-private-key.pem"),
    )
    parser.add_argument(
        "--jwt-public-key-file",
        type=Path,
        default=Path("./secrets/songdb-auth-public-key.pem"),
    )
    parser.add_argument(
        "--https-cert-file",
        type=Path,
        default=Path("./secrets/cert.pem"),
    )
    parser.add_argument(
        "--https-key-file",
        type=Path,
        default=Path("./secrets/key.pem"),
    )
    args = parser.parse_args()
    generate_password(args.mariadb_password_file, overwrite=args.overwrite)
    generate_password(args.mariadb_root_password_file, overwrite=args.overwrite)
    generate_es256_key_pair(
        args.jwt_private_key_file, args.jwt_public_key_file, overwrite=args.overwrite
    )
    generate_self_signed_cert(
        args.https_cert_file, args.https_key_file, overwrite=args.overwrite
    )
