# Song Database

This repository and the apps inside it are just a test for how I would want to design cloud-based services.

Note that this repository is just a toy example, and should not be used in production environments.

## Docker commands

```bash
# Run unit tests in Podman Compose
podman compose --profile test up --abort-on-container-exit
podman compose --profile test down
```
