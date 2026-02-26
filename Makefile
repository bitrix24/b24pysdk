.DEFAULT_GOAL := help

PYTHON_VERSION ?= 3.14
# CI image (bakes in sources) used in GitHub Actions only
CI_IMAGE ?= b24pysdk-ci
# Dev image (no sources baked) for local iterative dev with bind mounts
DEV_IMAGE ?= b24pysdk-dev
# Test image for your local tests
TEST_IMAGE ?= b24pysdk-test
M ?=
TEST_PATH ?=

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
	@echo "  test-scope    Run tests with path or marker (e.g., M='integration')"

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

build-test:
	docker build -f docker/test.Dockerfile -t $(TEST_IMAGE) --build-arg PYTHON_VERSION=$(PYTHON_VERSION) .

# Build dev image only if it's missing
ensure-dev-image:
	@docker image inspect $(DEV_IMAGE) > /dev/null 2>&1 || \
	  docker build -f docker/dev.Dockerfile -t $(DEV_IMAGE) --build-arg PYTHON_VERSION=$(PYTHON_VERSION) .

# Build CI image only if it's missing
ensure-ci-image:
	@docker image inspect $(CI_IMAGE) > /dev/null 2>&1 || \
	  docker build -f docker/ci.Dockerfile -t $(CI_IMAGE) --build-arg PYTHON_VERSION=$(PYTHON_VERSION) .

# Run all tests in the project
test-all: build-test
	docker run --rm -t \
		--env-file .env.local \
		$(TEST_IMAGE) \
		--cov=b24pysdk \
		tests/

# Run tests located in the tests/integration directory
test-integration: build-test
	docker run --rm -t \
		--env-file .env.local \
		$(TEST_IMAGE) tests/integration

# Run integration tests with AUTH_TYPE set to webhook
test-integration-webhook: build-test
	docker run --rm -t \
		--env-file .env.local \
		-e PREFER_AUTH_TYPE=webhook \
		$(TEST_IMAGE) tests/integration

# Run integration tests with AUTH_TYPE set to oauth
test-integration-oauth: build-test
	docker run --rm -t \
		--env-file .env.local \
		-e PREFER_AUTH_TYPE=oauth \
		$(TEST_IMAGE) tests/integration

# Execute all unit tests located in the tests/integration/unit directory
test-unit: build-test
	docker run --rm -t \
		--env-file .env.local \
		$(TEST_IMAGE) tests/integration/unit

# Run tests filtered by a specific pytest marker
test-marker: build-test
	docker run --rm -t \
		--env-file .env.local \
		$(TEST_IMAGE) -m $(M)

# Run tests located at a specific path provided as an argument
test-path: build-test
	docker run --rm -t \
		--env-file .env.local \
		$(TEST_IMAGE) $(TEST_PATH)

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
