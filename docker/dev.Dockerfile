# Dev container for running lint/tests via bind mounts (no source COPY)
# Usage: build once, then run with -v "$PWD:/work" so code/logs stay on host.

ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /work

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip \
    # Preinstall runtime dep used during dynamic version import
    && pip install requests \
    # Dev/test tooling only; project installed in run step with -e
    && pip install ruff pytest pytest-cov pytest-mock pytest-dependency

# Default command is a shell; Makefile will override with run commands
CMD ["bash"]
