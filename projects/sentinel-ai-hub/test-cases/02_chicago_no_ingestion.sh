#!/bin/bash
# Goal: Verify the AI responds gracefully when no SLA exists for Chicago.

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

echo "--- STARTING TEST CASE 2: CHICAGO (NO SLA) ---"
"$SCRIPT_DIR/../venv/bin/python3" "$SCRIPT_DIR/../scripts/simulate_event.py" "Blizzard" "Chicago" 8 "Heavy snowfall impacting terminal 5 logistics."
echo "--- TEST CASE 2 COMPLETE ---"
