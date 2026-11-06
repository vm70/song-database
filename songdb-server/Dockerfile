FROM python:3.13-slim as base

ENV PIP_ROOT_USER_ACTION=ignore

RUN useradd songdb
WORKDIR /opt/songdb-server
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
COPY ./src .
COPY ./pyproject.toml .
RUN --mount=type=cache,target=/root/.cache/pip pip install .

USER songdb
EXPOSE 8000
CMD [ "uvicorn", "songdb_server.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000" ]

FROM base as test

USER root
COPY ./test .
COPY requirements.dev.txt .
RUN --mount=type=cache,target=/home/songdb/.cache/pip pip install -r requirements.dev.txt
RUN --mount=type=cache,target=/home/songdb/.cache/pip pip install .

USER songdb
CMD [ "pytest", "." ]