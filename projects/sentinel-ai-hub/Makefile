.PHONY: setup provision ingest simulate run docker-build docker-run help venv

# Variables
IMAGE_NAME = sentinel-ai-hub
DOC_FILE = SLA_Warehouse_Miami.md
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3

# Set PYTHONPATH to the current directory to enable "app." absolute imports
export PYTHONPATH := $(shell pwd)

help:
	@echo "--- Project Sentinel Automation ---"
	@echo "venv           - Create the local virtual environment"
	@echo "setup          - Install dependencies (auto-creates venv)"
	@echo "provision      - Create the Azure AI Search index (Hybrid Search)"
	@echo "ingest         - Process the sample SLA into the Search Index"
	@echo "simulate       - Send a test disruption event to Event Hub"
	@echo "run            - Start the Sentinel Orchestrator (Main App)"
	@echo "docker-build   - Build the Sentinel Docker image"
	@echo "docker-run     - Run the Sentinel simulation in a container"
	@echo "-----------------------------------"

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

venv: $(VENV)/bin/activate

setup: venv
	$(PIP) install -r requirements.txt
	# Ensure Node.js is present for MCP servers (Slack/Maps)
	npx --version || (echo "Error: Node.js/npx not found. Please install Node.js." && exit 1)

provision: venv
	$(PYTHON) scripts/provision_search.py

ingest: venv
	$(PYTHON) scripts/ingest_doc.py $(DOC_FILE)

simulate: venv
	$(PYTHON) scripts/simulate_event.py

run: venv
	$(PYTHON) app/main.py

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run --env-file .env $(IMAGE_NAME)
