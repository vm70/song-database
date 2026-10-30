#!/bin/bash
#
# Populate the `secrets` directory with example secret files.
#
# Usage:
#
# ```bash
# ./scripts/create_test_secrets.sh
# ```

openssl rand -base64 20 >./secrets/songdb-mariadb-password
openssl rand -base64 20 >./secrets/songdb-mariadb-root-password
openssl ecparam -name prime256v1 -genkey -noout -out ./secrets/songdb-auth-private-key.pem
openssl ec -in ./secrets/songdb-auth-private-key.pem -pubout -out ./secrets/songdb-auth-public-key.pem
