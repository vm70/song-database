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
    uv run scripts/generate_secrets.py

# Run tests locally
[group("test")]
test-local: generate-secrets
    cp .env.local .env
    uv run pytest .

# Run tests in Podman / Docker
[group("test")]
test-containerized: generate-secrets
    cp .env.example .env
    docker compose --file compose.yml --file compose.test.yml run --build --rm songdb-server
    docker compose --file compose.yml --file compose.test.yml down --rmi local --volumes
    docker compose --file compose.yml --file compose.prod.yml up --detach
    docker compose --file compose.yml --file compose.prod.yml down

# Generate Python OpenAPI client
generate-client:
    cp .env.local .env
    uv run songdb-server --export-openapi doc/generated/openapi.json
    uv run openapi-generator-cli generate --input-spec doc/generated/openapi.json --generator-name python --minimal-update --output songdb-client
