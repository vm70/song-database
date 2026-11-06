# Song Database

This is a simple test application that I'm making to teach myself a proper structure for building cloud-based / containerized applications.

> [!WARNING]  
> This is a toy example, so it's probably not safe for production use. If you want to spin up your own pre-made production application, take a look at the [full-stack FastAPI template](https://github.com/fastapi/full-stack-fastapi-template).

This project uses `just` as a script runner.

## Running the Song Database

```bash
just run
```

## Running Unit Tests

Unit tests should work in both containerized and non-containerized environments.

```bash
just test
```

## Generating OpenAPI Client

This project will automatically generate an OpenAPI client.

```bash
just generate-openapi-client
```
