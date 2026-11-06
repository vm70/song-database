FROM python:3.13-slim as base

ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /opt/songdb-server
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
COPY ./src .
COPY ./pyproject.toml .
RUN --mount=type=cache,target=/root/.cache/pip pip install .

EXPOSE 8000
CMD [ "fastapi", "run", "src/songdb_server/api/app.py" ]

FROM base as test

COPY ./test .
COPY requirements.dev.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.dev.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install .

CMD [ "pytest", "." ]