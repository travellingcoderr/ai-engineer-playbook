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
RESEARCH_PORT ?= 8003
MULTI_AGENT_PORT ?= 8004
GUARD_PORT ?= 8005
RESILIENT_GATEWAY_PORT ?= 8006
N8N_PORT ?= 5678
PERF_EVAL_PORT ?= 8007
DASHBOARD_PORT ?= 8080

# Infrastructure Ports
QDRANT_PORT ?= 6333
MONGO_PORT ?= 27017
REDIS_PORT ?= 6379

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

# Rag System
run-rag:
	@$(ACTIVATE) && PYTHONPATH=$(PWD)/projects/rag_system uvicorn projects.rag_system.app.main:app \
	--host 127.0.0.1 \
	--port $(RAG_PORT) \
	--reload \
	--reload-dir projects/rag_system

run-docker-rag:
	@echo "Starting RAG system via Docker Compose..."
	cd projects/rag_system && docker-compose up -d --build

stop-docker-rag:
	@echo "Stopping RAG system Docker containers..."
	cd projects/rag_system && docker-compose down

# MCP Gateway
run-mcp:
	@$(ACTIVATE) && PYTHONPATH=$(PWD)/projects/mcp_gateway uvicorn projects.mcp_gateway.app.main:app \
	--host 127.0.0.1 \
	--port $(GATEWAY_PORT) \
	--reload \
	--reload-dir projects/mcp_gateway

run-docker-gateway:
	@echo "Starting MCP Gateway via Docker Compose..."
	cd projects/mcp_gateway && docker-compose up -d --build

stop-docker-gateway:
	@echo "Stopping MCP Gateway Docker containers..."
	cd projects/mcp_gateway && docker-compose down

# Observability
run-observe:
	@$(ACTIVATE) && PYTHONPATH=$(PWD)/projects/observability uvicorn projects.observability.api:app \
	--host 127.0.0.1 \
	--port $(OBS_PORT) \
	--reload \
	--reload-dir projects/observability

run-docker-observe:
	@echo "Starting Observability via Docker Compose..."
	cd projects/observability && docker-compose up -d --build

stop-docker-observe:
	@echo "Stopping Observability Docker containers..."
	cd projects/observability && docker-compose down

# Research Agent
run-research:
	@$(ACTIVATE) && PYTHONPATH=$(PWD)/projects/research_agent uvicorn projects.research_agent.app.main:app \
	--host 127.0.0.1 \
	--port $(RESEARCH_PORT) \
	--reload \
	--reload-dir projects/research_agent

run-docker-research:
	@echo "Starting Research Agent via Docker Compose..."
	cd projects/research_agent && docker-compose up -d --build

stop-docker-research:
	@echo "Stopping Research Agent Docker containers..."
	cd projects/research_agent && docker-compose down

# Multi-Agent Orchestrator
run-multi-agent:
	@$(ACTIVATE) && PYTHONPATH=$(PWD)/projects/multi_agent uvicorn projects.multi_agent.app.main:app \
	--host 127.0.0.1 \
	--port $(MULTI_AGENT_PORT) \
	--reload \
	--reload-dir projects/multi_agent

run-docker-multi-agent:
	@echo "Starting Multi-Agent Orchestrator via Docker Compose..."
	cd projects/multi_agent && docker-compose up -d --build

stop-docker-multi-agent:
	@echo "Stopping Multi-Agent Orchestrator Docker containers..."
	cd projects/multi_agent && docker-compose down

# Guardrails
run-guardrails:
	@$(ACTIVATE) && PYTHONPATH=$(PWD)/projects/guardrails uvicorn projects.guardrails.app.main:app \
	--host 127.0.0.1 \
	--port $(GUARD_PORT) \
	--reload \
	--reload-dir projects/guardrails

run-docker-guardrails:
	@echo "Starting Guardrails via Docker Compose..."
	cd projects/guardrails && docker-compose up -d --build

stop-docker-guardrails:
	@echo "Stopping Guardrails Docker containers..."
	cd projects/guardrails && docker-compose down

# Resilient AI Gateway
run-resilient-gateway:
	@$(ACTIVATE) && PYTHONPATH=$(PWD):$(PWD)/projects/resilient_gateway uvicorn projects.resilient_gateway.app.main:app \
	--host 127.0.0.1 \
	--port $(RESILIENT_GATEWAY_PORT) \
	--reload \
	--reload-dir projects/resilient_gateway

run-docker-resilient-gateway:
	@echo "Starting Resilient AI Gateway via Docker Compose..."
	cd projects/resilient_gateway && docker-compose up -d --build

stop-docker-resilient-gateway:
	@echo "Stopping Resilient AI Gateway Docker containers..."
	cd projects/resilient_gateway && docker-compose down

# workflow_orchestrator (n8n)
run-n8n:
	@echo "Starting n8n Workflow Orchestrator..."
	@cd projects/workflow_orchestrator && docker-compose up -d
	@echo "n8n is running at http://localhost:$(N8N_PORT)"

stop-n8n:
	@echo "Stopping n8n Workflow Orchestrator..."
	@cd projects/workflow_orchestrator && docker-compose down

# ai_perf_eval
run-perf-eval:
	@echo "Starting AI Performance & Evaluation Service..."
	@cd projects/ai_perf_eval && PYTHONPATH=$(PWD):$(PWD)/projects/ai_perf_eval python3 app/main.py

run-docker-perf-eval:
	@echo "Starting AI Performance & Evaluation in Docker..."
	@cd projects/ai_perf_eval && docker-compose up --build -d

stop-docker-perf-eval:
	@echo "Stopping AI Performance & Evaluation in Docker..."
	@cd projects/ai_perf_eval && docker-compose down

# Infrastructure (Qdrant, Mongo, Redis)
run-infra:
	@echo "Starting Shared Infrastructure (Qdrant, Mongo, Redis)..."
	@cd projects/infrastructure && docker-compose up -d

stop-infra:
	@echo "Stopping Shared Infrastructure..."
	@cd projects/infrastructure && docker-compose down

# Observability Logs
tail-observe-logs:
	@docker logs -f observability_api

# Dashboard
run-dashboard:
	@$(ACTIVATE) && PYTHONPATH=$(PWD) uvicorn dashboard.main:app \
	--host 127.0.0.1 \
	--port $(DASHBOARD_PORT) \
	--reload \
	--reload-dir dashboard

# ==============================
# Run All Services
# ==============================

run-all:
	@echo "Starting RAG service..."
	@$(ACTIVATE) && PYTHONPATH=$(PWD)/projects/rag_system uvicorn projects.rag_system.app.main:app \
	--port $(RAG_PORT) --reload --reload-dir projects/rag_system \
	> rag.log 2>&1 & echo $$! > rag.pid

	@echo "Starting MCP gateway..."
	@$(ACTIVATE) && PYTHONPATH=$(PWD)/projects/mcp_gateway uvicorn projects.mcp_gateway.app.main:app \
	--port $(GATEWAY_PORT) --reload --reload-dir projects/mcp_gateway \
	> gateway.log 2>&1 & echo $$! > gateway.pid

	@echo "Starting Observability service..."
	@$(ACTIVATE) && PYTHONPATH=$(PWD)/projects/observability uvicorn projects.observability.api:app \
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
	@echo "Running root tests..."
	@$(ACTIVATE) && python3 -m pytest tests/ -q
	@for dir in projects/*; do \
		if [ -d "$$dir/tests" ]; then \
			project=$$(basename $$dir); \
			echo "Running $$project tests..."; \
			PYTHONPATH=$(PWD):$(PWD)/$$dir $(ACTIVATE) && python3 -m pytest $$dir/tests/ -q || exit 1; \
		fi \
	done

lint:
	@$(ACTIVATE) && ruff check .

eval:
	@echo "Running AI Evaluations for RAG System..."
	@$(ACTIVATE) && PYTHONPATH=$(PWD):$(PWD)/projects/rag_system python3 projects/rag_system/evals/eval_runner.py

# (Duplicate removed as it's now run-resilient-gateway)

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

kill-mcp:
	@make kill-port PORT=$(GATEWAY_PORT)

kill-observe:
	@make kill-port PORT=$(OBS_PORT)

kill-research:
	@make kill-port PORT=$(RESEARCH_PORT)

kill-multi-agent:
	@make kill-port PORT=$(MULTI_AGENT_PORT)

kill-dashboard:
	@make kill-port PORT=$(DASHBOARD_PORT)

kill-guardrails:
	@make kill-port PORT=$(GUARD_PORT)

kill-resilient-gateway:
	@make kill-port PORT=$(RESILIENT_GATEWAY_PORT)

kill-n8n:
	@make kill-port PORT=$(N8N_PORT)

kill-perf-eval:
	@make kill-port PORT=$(PERF_EVAL_PORT)

kill-infra:
	@make kill-port PORT=$(QDRANT_PORT)
	@make kill-port PORT=$(MONGO_PORT)
	@make kill-port PORT=$(REDIS_PORT)

kill-all:
	@make kill-rag
	@make kill-mcp
	@make kill-observe
	@make kill-multi-agent
	@make kill-dashboard
	@make kill-research
	@make kill-resilient-gateway
	@make kill-guardrails
	@make kill-n8n