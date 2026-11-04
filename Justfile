#!/usr/bin/env just --justfile

set shell := ["bash", "-c"]

# Display help information
default:
    @just --list

# Run all tests
test: test-local test-containerized

# Format everything
format:
    uv run black .
    uv run ruff format .
    prettier --write .

# Perform linting & type checking
lint:
    uv run ruff check . --fix
    uv run pyrefly check .

# Generate example secrets
generate-secrets:
    # Generate MariaDB user password
    if [[ ! -f ./secrets/songdb-mariadb-password ]]; then openssl rand -base64 20 >./secrets/songdb-mariadb-password; fi
    # Generate MariaDB root password
    if [[ ! -f ./secrets/songdb-mariadb-root-password ]]; then openssl rand -base64 20 >./secrets/songdb-mariadb-root-password; fi
    # Generate ES256 private key
    if [[ ! -f ./secrets/songdb-auth-private-key ]]; then openssl ecparam -name prime256v1 -genkey -noout -out ./secrets/songdb-auth-private-key.pem; fi
    # Generate ES256 public key
    if [[ ! -f ./secrets/songdb-auth-public-key ]]; then openssl ec -in ./secrets/songdb-auth-private-key.pem -pubout -out ./secrets/songdb-auth-public-key.pem; fi
    # Generate HTTPS certificate
    if [[ ! -f ./secrets/cert.pem ]] || [[ ! -f ./secrets/key.pem ]]; then openssl req -x509 -newkey rsa:4096 -nodes -subj "/ST=./L=./O=./OU=./CN=." -out ./secrets/cert.pem -keyout ./secrets/key.pem -days 365; fi

# Run tests locally
[group("test")]
test-local: generate-secrets
    cp .env.local .env
    uv run pytest .

# Run tests in Podman / Docker
[group("test")]
test-containerized: generate-secrets
    cp .env.example .env
    docker compose --profile test up --build --abort-on-container-exit
    docker compose --profile test down --rmi local --volumes

# Generate Python OpenAPI client
generate-client:
    uv run songdb-server --export-openapi doc/generated/openapi.json
    uv run openapi-generator-cli generate --input-spec doc/generate
