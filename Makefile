.PHONY: up down build lint test eval dev help

PYTHON := .venv/bin/python
PIP := .venv/bin/pip
RUFF := .venv/bin/ruff
MYPY := .venv/bin/mypy
PYTEST := .venv/bin/pytest
COMPOSE := docker compose

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

up: ## Démarre tous les services (Qdrant + Ollama + API)
	$(COMPOSE) up -d --build
	@echo "API  → http://localhost:8000"
	@echo "Docs → http://localhost:8000/docs"
	@echo "Qdrant → http://localhost:6333"

down: ## Arrête tous les services
	$(COMPOSE) down

build: ## Build l'image Docker API
	$(COMPOSE) build api

logs: ## Affiche les logs de tous les services
	$(COMPOSE) logs -f

lint: ## Lint (ruff) + type-check (mypy)
	$(RUFF) check .
	$(RUFF) format --check .
	$(MYPY) src/

format: ## Formate le code avec ruff
	$(RUFF) format .
	$(RUFF) check --fix .

test: ## Lance pytest
	$(PYTEST)

test-cov: ## Lance pytest avec couverture
	$(PYTEST) --cov=coursegraph --cov-report=html --cov-report=term-missing

eval: ## Lance le pipeline d'évaluation RAGAS
	$(PYTHON) eval/run_eval.py

dev: ## Lance Streamlit en développement local
	.venv/bin/streamlit run app/streamlit_app.py

install: ## Crée le venv et installe les dépendances de dev
	python3 -m venv .venv
	$(PIP) install -e ".[dev]"

pull-models: ## Télécharge les modèles Ollama requis
	$(COMPOSE) exec ollama ollama pull mistral:7b-instruct
	$(COMPOSE) exec ollama ollama pull qwen2.5:3b-instruct
