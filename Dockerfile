FROM python:3.13-slim

COPY ./pyproject.toml .
COPY ./poetry.lock .
COPY ./.flake8 .
COPY ./.isort.cfg .

RUN apt-get update && apt-get install -y \
    build-essential \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

WORKDIR /app

COPY app /app
