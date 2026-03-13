#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Bootstrapping sample MCP gateway..."
cd "$ROOT_DIR/mcp-gateway"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Done. Activate with: source $ROOT_DIR/mcp-gateway/.venv/bin/activate"
echo "Run with: uvicorn app.main:app --reload"
