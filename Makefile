.PHONY: help install test lint format clean setup docker-neo4j

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Set up the project (install dependencies, create .env)
	python3 setup.py

install: ## Install dependencies using Poetry
	poetry install

test: ## Run tests
	poetry run pytest tests/ -v

test-cov: ## Run tests with coverage
	poetry run pytest tests/ --cov=neo4j_learning --cov-report=html --cov-report=term-missing

lint: ## Run linting checks
	poetry run flake8 neo4j_learning/ tests/
	poetry run mypy neo4j_learning/

format: ## Format code using Black
	poetry run black neo4j_learning/ tests/

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .mypy_cache/

docker-neo4j: ## Start Neo4j in Docker
	docker run --name neo4j \
		-p 7474:7474 -p 7687:7687 \
		-e NEO4J_AUTH=neo4j/password \
		-e NEO4J_PLUGINS='["apoc"]' \
		-d neo4j:5.15.0

docker-neo4j-stop: ## Stop Neo4j Docker container
	docker stop neo4j
	docker rm neo4j

test-connection: ## Test Neo4j connection
	poetry run python -m neo4j_learning.cli test

examples: ## Run learning examples
	poetry run python -m neo4j_learning.cli examples

interactive: ## Start interactive Neo4j CLI
	poetry run python -m neo4j_learning.cli interactive

clear-db: ## Clear all data from Neo4j database
	poetry run python -m neo4j_learning.cli clear

dev: ## Run all development checks (format, lint, test)
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test 