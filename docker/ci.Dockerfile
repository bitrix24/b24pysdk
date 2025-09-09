# syntax=docker/dockerfile:1.6

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (git for editable installs if needed)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Copy only project metadata first (leverage Docker layer caching)
COPY pyproject.toml README.md LICENSE /app/
COPY b24pysdk/ /app/b24pysdk/
COPY tests/ /app/tests/

# Install project and dev/test tooling
RUN python -m pip install --upgrade pip \
 && pip install requests \
 && pip install .[dev,test]

# Default command runs lint + tests; can be overridden in CI
CMD ["bash", "-lc", "ruff check . && pytest -q"]
