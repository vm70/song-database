FROM python:3.13-slim

ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /opt/songdb-server
COPY ./ .
RUN pip install --no-cache-dir .
EXPOSE 8000
CMD [ "fastapi", "run", "src/songdb_server/api/app.py" ]