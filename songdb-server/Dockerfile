FROM python:3.13-slim

ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /opt/songdb-server
COPY requirements.txt ./requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
COPY ./ .
RUN rm -rf ./test
RUN --mount=type=cache,target=/root/.cache/pip pip install .

EXPOSE 8000
CMD [ "fastapi", "run", "src/songdb_server/api/app.py" ]