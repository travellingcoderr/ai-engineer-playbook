#!/bin/bash
# Goal: Ingest a simulated Chicago SLA into Azure AI Search.

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

echo "--- STARTING TEST CASE 3: INGEST CHICAGO ---"

# Step 1: Generate PDF
"$SCRIPT_DIR/../venv/bin/python3" "$SCRIPT_DIR/../scripts/generate_test_pdf.py" "Chicago Logistics" "Milwaukee-Backup" 6 12000

# Step 2: Ingest into Search
"$SCRIPT_DIR/../venv/bin/python3" "$SCRIPT_DIR/../scripts/ingest_doc.py" "$SCRIPT_DIR/../pdfs/chicago_logistics_sla.pdf"

echo "--- TEST CASE 3 COMPLETE ---"
