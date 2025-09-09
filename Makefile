.DEFAULT_GOAL := help

PYTHON_VERSION ?= 3.12
# CI image (bakes in sources) used in GitHub Actions only
CI_IMAGE ?= b24pysdk-ci
# Dev image (no sources baked) for local iterative dev with bind mounts
DEV_IMAGE ?= b24pysdk-dev

# If .env.local exists, use it; otherwise use .env; else none
ENV_FILE := $(firstword $(wildcard .env.local .env))
ENV_FILE_FLAG := $(if $(ENV_FILE),--env-file $(ENV_FILE),)

.PHONY: help build-ci test-ci shell-ci ensure-ci-image build-dev ensure-dev-image test test-int test-int-webhook test-int-oauth lint shell

help: ## Show this help
	@echo "Available targets:"
	@echo "  build-dev      Build the dev image (tools only; no sources baked)"
	@echo "  ensure-dev-image  Build dev image only if missing"
	@echo "  test           Run pytest inside dev container (mounts repo; no rebuild)"
	@echo "  test-int       Run integration tests (-m integration); uses .env if present"
	@echo "  lint           Run ruff lint inside dev container (mounts repo)"
	@echo "  shell          Interactive shell in dev container (mounts repo)"
	@echo "  build-ci       Build the CI image (bakes sources; mirrors CI)"
	@echo "  ensure-ci-image  Build CI image only if missing"
	@echo "  test-ci        Run baked CI image (rarely needed locally)"
	@echo "  shell-ci       Interactive shell in CI image"

# Build once: CI image (kept for parity with CI)
build-ci:
	docker build -f docker/ci.Dockerfile -t $(CI_IMAGE) --build-arg PYTHON_VERSION=$(PYTHON_VERSION) .

# Run the baked CI image (rarely needed locally)
test-ci: ensure-ci-image
	docker run --rm -t $(CI_IMAGE)

# Optional: get an interactive shell in the CI image
shell-ci: ensure-ci-image
	docker run --rm -it $(CI_IMAGE) bash

# Build once: Dev image with tools only; no sources copied
build-dev:
	docker build -f docker/dev.Dockerfile -t $(DEV_IMAGE) --build-arg PYTHON_VERSION=$(PYTHON_VERSION) .

# Build dev image only if it's missing
ensure-dev-image:
	@docker image inspect $(DEV_IMAGE) > /dev/null 2>&1 || \
	  docker build -f docker/dev.Dockerfile -t $(DEV_IMAGE) --build-arg PYTHON_VERSION=$(PYTHON_VERSION) .

# Build CI image only if it's missing
ensure-ci-image:
	@docker image inspect $(CI_IMAGE) > /dev/null 2>&1 || \
	  docker build -f docker/ci.Dockerfile -t $(CI_IMAGE) --build-arg PYTHON_VERSION=$(PYTHON_VERSION) .

# Mount repo; install package in editable mode; run tests. No rebuild on code change.
test: ensure-dev-image
	docker run --rm -t \
	  -v "$(PWD):/work" \
	  -w /work \
	  $(DEV_IMAGE) \
	  bash -lc "pip install -e .[test] && pytest -q"

# Run only integration tests; uses .env automatically if present
test-int: ensure-dev-image
	@if [ -n "$(ENV_FILE)" ]; then echo "Using env file: $(ENV_FILE)"; fi
	docker run --rm -t $(ENV_FILE_FLAG) \
	  -v "$(PWD):/work" \
	  -w /work \
	  $(DEV_IMAGE) \
	  bash -lc "pip install -e .[test] && pytest -m integration -vv -rA"

# Run integration tests with webhook creds provided via variables
# Usage: make test-int-webhook B24_DOMAIN=... B24_WEBHOOK=...
test-int-webhook: ensure-dev-image
	@if [ -z "$(B24_DOMAIN)" ] || [ -z "$(B24_WEBHOOK)" ]; then \
	  echo "Set B24_DOMAIN and B24_WEBHOOK variables"; exit 2; \
	fi
	docker run --rm -t \
	  -e B24_PREFER=webhook \
	  -e B24_DOMAIN="$(B24_DOMAIN)" \
	  -e B24_WEBHOOK="$(B24_WEBHOOK)" \
	  -v "$(PWD):/work" \
	  -w /work \
	  $(DEV_IMAGE) \
	  bash -lc "pip install -e .[test] && pytest -q -m integration"

# Run integration tests with OAuth creds provided via variables
# Usage: make test-int-oauth B24_DOMAIN=... B24_CLIENT_ID=... B24_CLIENT_SECRET=... B24_ACCESS_TOKEN=... [B24_REFRESH_TOKEN=...]
test-int-oauth: ensure-dev-image
	@if [ -z "$(B24_DOMAIN)" ] || [ -z "$(B24_CLIENT_ID)" ] || [ -z "$(B24_CLIENT_SECRET)" ] || [ -z "$(B24_ACCESS_TOKEN)" ]; then \
	  echo "Set B24_DOMAIN, B24_CLIENT_ID, B24_CLIENT_SECRET, B24_ACCESS_TOKEN (and optionally B24_REFRESH_TOKEN)"; exit 2; \
	fi
	docker run --rm -t \
	  -e B24_PREFER=oauth \
	  -e B24_DOMAIN="$(B24_DOMAIN)" \
	  -e B24_CLIENT_ID="$(B24_CLIENT_ID)" \
	  -e B24_CLIENT_SECRET="$(B24_CLIENT_SECRET)" \
	  -e B24_ACCESS_TOKEN="$(B24_ACCESS_TOKEN)" \
	  -e B24_REFRESH_TOKEN="$(B24_REFRESH_TOKEN)" \
	  -v "$(PWD):/work" \
	  -w /work \
	  $(DEV_IMAGE) \
	  bash -lc "pip install -e .[test] && pytest -q -m integration"

# Mount repo; run linter on host files. No rebuild on code change.
lint: ensure-dev-image
	docker run --rm -t \
	  -v "$(PWD):/work" \
	  -w /work \
	  $(DEV_IMAGE) \
	  ruff check .

# Optional interactive dev shell with repo mounted
shell: ensure-dev-image
	docker run --rm -it \
	  -v "$(PWD):/work" \
	  -w /work \
	  $(DEV_IMAGE) bash
