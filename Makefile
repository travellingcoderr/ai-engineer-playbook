.PHONY: env setup install run-rag run-gateway run-observe run-all stop-all test lint clean kill-port kill-rag kill-gateway kill-observe kill-all

PYTHON := python3
VENV := .venv
ACTIVATE := . $(VENV)/bin/activate

# ==============================
# Ports
# ==============================

RAG_PORT ?= 8000
GATEWAY_PORT ?= 8001
OBS_PORT ?= 8002

# ==============================
# Environment Setup
# ==============================

env:
	@if [ ! -f .env ]; then \
		echo "Creating .env from .env.example"; \
		cp .env.example .env; \
	else \
		echo ".env already exists"; \
	fi

setup: env
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
	fi
	@$(ACTIVATE) && pip install --upgrade pip
	@$(ACTIVATE) && pip install -r requirements.txt

install: setup

# ==============================
# Run Services
# ==============================

run-rag:
	@$(ACTIVATE) && uvicorn projects.rag_system.app.main:app \
	--host 127.0.0.1 \
	--port $(RAG_PORT) \
	--reload \
	--reload-dir projects/rag_system

run-gateway:
	@$(ACTIVATE) && uvicorn projects.mcp_gateway.app.main:app \
	--host 127.0.0.1 \
	--port $(GATEWAY_PORT) \
	--reload \
	--reload-dir projects/mcp_gateway

run-observe:
	@$(ACTIVATE) && uvicorn projects.observability.api:app \
	--host 127.0.0.1 \
	--port $(OBS_PORT) \
	--reload \
	--reload-dir projects/observability

# ==============================
# Run All Services
# ==============================

run-all:
	@echo "Starting RAG service..."
	@$(ACTIVATE) && uvicorn projects.rag_system.app.main:app \
	--port $(RAG_PORT) --reload --reload-dir projects/rag_system \
	> rag.log 2>&1 & echo $$! > rag.pid

	@echo "Starting MCP gateway..."
	@$(ACTIVATE) && uvicorn projects.mcp_gateway.app.main:app \
	--port $(GATEWAY_PORT) --reload --reload-dir projects/mcp_gateway \
	> gateway.log 2>&1 & echo $$! > gateway.pid

	@echo "Starting Observability service..."
	@$(ACTIVATE) && uvicorn projects.observability.api:app \
	--port $(OBS_PORT) --reload --reload-dir projects/observability \
	> observe.log 2>&1 & echo $$! > observe.pid

	@echo "All services started"

# ==============================
# Stop Services
# ==============================

stop-all:
	@echo "Stopping services..."

	@if [ -f rag.pid ]; then kill `cat rag.pid` && rm rag.pid; fi
	@if [ -f gateway.pid ]; then kill `cat gateway.pid` && rm gateway.pid; fi
	@if [ -f observe.pid ]; then kill `cat observe.pid` && rm observe.pid; fi

	@echo "All services stopped"

# ==============================
# Utilities
# ==============================

test:
	@$(ACTIVATE) && pytest -q

lint:
	@$(ACTIVATE) && ruff check .

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache rag.pid gateway.pid observe.pid

# ==============================
# Kill Ports
# ==============================

kill-port:
	@if [ -z "$(PORT)" ]; then \
		echo "Usage: make kill-port PORT=<port_number>"; \
		exit 1; \
	fi
	@PID=$$(lsof -t -i:$(PORT)); \
	if [ -n "$$PID" ]; then \
		echo "Killing process $$PID on port $(PORT)"; \
		kill -9 $$PID; \
	else \
		echo "No process running on port $(PORT)"; \
	fi

kill-rag:
	@make kill-port PORT=$(RAG_PORT)

kill-gateway:
	@make kill-port PORT=$(GATEWAY_PORT)

kill-observe:
	@make kill-port PORT=$(OBS_PORT)

kill-all:
	@make kill-rag
	@make kill-gateway
	@make kill-observe