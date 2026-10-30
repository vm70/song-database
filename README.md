# Song Database

This is a simple test application that I'm making to teach myself a proper structure for building cloud-based / containerized applications.

> [!WARNING]  
> This is a toy example, so it's probably not safe for production use. If you want to spin up your own pre-made production application, take a look at the [full-stack FastAPI template](https://github.com/fastapi/full-stack-fastapi-template).

## Docker Commands

```bash
# Run unit tests in Podman Compose
podman compose --profile test up --abort-on-container-exit
podman compose --profile test down
```

## Client Generation

```bash
uv run openapi-generator-cli generate /
    --input-spec doc/generated/openapi.json /
    --generator-name python /
    --minimal-update /
    --output /
    songdb-client
```
