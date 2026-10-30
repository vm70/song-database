#!/bin/bash

echo -n "user-password" > ./secrets/songdb-mariadb-password
echo -n "root-password" > ./secrets/songdb-mariadb-root-password
openssl ecparam -name prime256v1 -genkey -noout -out ./secrets/songdb-auth-private-key.pem
openssl ec -in ./secrets/songdb-auth-private-key.pem -pubout -out ./secrets/songdb-auth-public-key.pem