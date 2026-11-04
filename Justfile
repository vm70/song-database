# Test everything
test-all: test-local test-containerized

# Run tests locally
test-local:
    ./scripts/create_test_secrets.sh
    cp .env.local .env
    uv run pytest .

# Run tests in Podman / Docker
test-containerized:
    ./scripts/create_test_secrets.sh
    cp .env.example .env
    docker compose --profile test up --build --abort-on-container-exit
    docker compose --profile test down --rmi local --volumes

# Generate OpenAPI client
generate-client:
    uv run songdb-server --export-openapi doc/generated/openapi.json
    uv run openapi-generator-cli generate --input-spec doc/generated/openapi.json --generator-name python --minimal-update --output songdb-client