#!/bin/bash

openssl rand --base64 32 > ./secrets/songdb-auth-secret-key
echo -n "user-password" > ./secrets/songdb-mariadb-password
echo -n "root-password" > ./secrets/songdb-mariadb-root-password