FROM python:3.12-slim as builder
LABEL maintainer="L M Sandt <laurens.sandt@protonmail.com>"

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN python -m venv /venv

ENV POETRY_VERSION=1.5.1
ENV POETRY_HOME=/opt/poetry
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /app
COPY pyproject.toml poetry.lock ./
# COPY migrations .
RUN . /venv/bin/activate; \
    $POETRY_HOME/bin/poetry install 


FROM python:3.12-slim as final

COPY --from=builder /venv /venv
ENV PATH=/venv/bin:${PATH}

WORKDIR /app
USER nobody

# docker-compose exec backend aerich migrate / upgrade are the commands to update the database after
# changes in the models are made!