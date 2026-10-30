#!/bin/bash
#
# Populate the `secrets` directory with the required secret files.
#
# Usage:
#
# ```bash
# ./scripts/create_test_secrets.sh 
# ```

echo -n "user-password" > ./secrets/songdb-mariadb-password
echo -n "root-password" > ./secrets/songdb-mariadb-root-password
openssl ecparam -name prime256v1 -genkey -noout -out ./secrets/songdb-auth-private-key.pem
openssl ec -in ./secrets/songdb-auth-private-key.pem -pubout -out ./secrets/songdb-auth-public-key.pem