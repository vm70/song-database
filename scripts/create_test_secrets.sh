#!/bin/bash
#
# Populate the `secrets` directory with example secret files.
#
# Usage:
#
# ```bash
# ./scripts/create_test_secrets.sh
# ```

# Generate passwords
openssl rand -base64 20 >./secrets/songdb-mariadb-password
openssl rand -base64 20 >./secrets/songdb-mariadb-root-password

# Generate ES256 key pair
openssl ecparam -name prime256v1 -genkey -noout -out ./secrets/songdb-auth-private-key.pem
openssl ec -in ./secrets/songdb-auth-private-key.pem -pubout -out ./secrets/songdb-auth-public-key.pem

# Generate HTTPS certificate
openssl req -x509 -newkey rsa:4096 -nodes -out ./secrets/cert.pem -keyout ./secrets/key.pem -days 365