.PHONY: help build up down logs test lint type-check format clean shell restart ps

help:
	@echo "Translation API - Docker Commands"
	@echo "=================================="
	@echo "  make build       - Build Docker image"
	@echo "  make up          - Start Docker containers"
	@echo "  make down        - Stop Docker containers"
	@echo "  make restart     - Restart containers"
	@echo "  make logs        - View container logs"
	@echo "  make ps          - Show running containers"
	@echo "  make test        - Run tests in container"
	@echo "  make lint        - Run linting"
	@echo "  make type-check  - Run type checking"
	@echo "  make format      - Format code"
	@echo "  make shell       - Open shell in container"
	@echo "  make clean       - Remove containers and images"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ Translator API is running at http://localhost:8000"
	@echo "📚 Documentation at http://localhost:8000/docs"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f translator-api

ps:
	docker-compose ps

test:
	docker-compose exec translator-api pytest -v

lint:
	docker-compose exec translator-api ruff check app/ tests/

type-check:
	docker-compose exec translator-api mypy app/

format:
	docker-compose exec translator-api ruff format app/ tests/

shell:
	docker-compose exec translator-api /bin/bash

clean:
	docker-compose down -v
	docker image rm translator_api-translator-api 2>/dev/null || true
	@echo "✅ Cleaned up Docker resources"

.DEFAULT_GOAL := help
