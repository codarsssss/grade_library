FROM python:3.13-slim

COPY ./pyproject.toml .
COPY ./poetry.lock .
COPY ./.flake8 .
COPY ./.isort.cfg .

RUN pip install -U pip && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

WORKDIR /app

COPY app /app
