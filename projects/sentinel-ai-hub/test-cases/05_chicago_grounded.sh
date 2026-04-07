#!/bin/bash
# Goal: Verify the AI responds with SLA data from the Chicago ingestion.

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

echo "--- STARTING TEST CASE 5: CHICAGO (GROUNDED) ---"
"$SCRIPT_DIR/../venv/bin/python3" "$SCRIPT_DIR/../scripts/simulate_event.py" "Blizzard" "Chicago" 8 "Major snowstorm threatening Chicago Warehouse operations."
echo "--- TEST CASE 5 COMPLETE ---"
echo "Observe: The ResponderAgent should now suggest 'Milwaukee-Backup' as your recovery hub!"
