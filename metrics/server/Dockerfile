FROM --platform=linux/amd64 python:3.8.9-slim-buster AS builder
WORKDIR /app

RUN pip install poetry
ADD pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-ansi --no-dev
ADD server /app/server

ENTRYPOINT ["/app/.venv/bin/uvicorn", "server.main:app"]