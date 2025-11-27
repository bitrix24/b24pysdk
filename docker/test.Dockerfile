ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip

COPY pyproject.toml /app/
COPY b24pysdk/ /app/b24pysdk/
COPY tests/ /app/tests/
COPY tests/oauth_data.json /app/

RUN pip install requests \
    && pip install ruff pytest pytest-cov pytest-mock pytest-dependency \
    && pip install .[dev,test]

ENTRYPOINT ["pytest"]