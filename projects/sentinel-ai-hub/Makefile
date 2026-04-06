.PHONY: setup provision ingest simulate run docker-build docker-run help

# Variables
IMAGE_NAME = sentinel-ai-hub
DOC_FILE = SLA_Warehouse_Miami.md

help:
	@echo "--- Project Sentinel Automation ---"
	@echo "setup          - Install local Python and Node dependencies"
	@echo "provision      - Create the Azure AI Search index (Hybrid Search)"
	@echo "ingest         - Process the sample SLA into the Search Index"
	@echo "simulate       - Send a test disruption event to Event Hub"
	@echo "run            - Start the Sentinel Orchestrator (Main App)"
	@echo "docker-build   - Build the Sentinel Docker image"
	@echo "docker-run     - Run the Sentinel simulation in a container"
	@echo "-----------------------------------"

setup:
	pip install -r requirements.txt
	# Ensure Node.js is present for MCP servers (Slack/Maps)
	npx --version || (echo "Error: Node.js/npx not found. Please install Node.js." && exit 1)

provision:
	python scripts/provision_search.py

ingest:
	python scripts/ingest_doc.py $(DOC_FILE)

simulate:
	python scripts/simulate_event.py

run:
	python app/main.py

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run --env-file .env $(IMAGE_NAME)
