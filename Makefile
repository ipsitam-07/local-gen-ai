.PHONY: help venv install dev test lint format typecheck docker-up docker-down docker-logs clean

PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

venv: ## Create virtual environment
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip setuptools wheel

install: venv ## Install project in editable mode with dev dependencies
	$(BIN)/pip install -e ".[dev]"

dev: ## Run local FastAPI server with hot-reload
	$(BIN)/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test: ## Run unit and integration tests
	$(BIN)/pytest -v

test-unit: ## Run only unit tests
	$(BIN)/pytest -v tests/unit

lint: ## Run Ruff linter
	$(BIN)/ruff check .

format: ## Run Ruff auto-formatter
	$(BIN)/ruff format .

typecheck: ## Run Mypy static type checker
	$(BIN)/mypy app

docker-up: ## Start all services in Docker Compose (detached)
	docker compose up -d

docker-down: ## Stop all Docker Compose services and retain volumes
	docker compose down

docker-down-v: ## Stop all Docker Compose services and delete volumes
	docker compose down -v

docker-logs: ## Tail logs from all Docker Compose services
	docker compose logs -f

clean: ## Clean Python cache and build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info
