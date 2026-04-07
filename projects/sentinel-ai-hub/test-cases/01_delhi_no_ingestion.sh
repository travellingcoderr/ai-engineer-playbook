#!/bin/bash
# Goal: Verify the AI responds gracefully when no SLA exists for the target city.

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

echo "--- STARTING TEST CASE 1: DELHI (NO SLA) ---"
"$SCRIPT_DIR/../venv/bin/python3" "$SCRIPT_DIR/../scripts/simulate_event.py" "Monsoon Flood" "Delhi" 7 "Heavy rainfall impacting logistics hub in Old Delhi."
echo "--- TEST CASE 1 COMPLETE ---"
echo "Check the Sentinel Orchestrator logs to see 'I cannot find a relevant clause' response."
