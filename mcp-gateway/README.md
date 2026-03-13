# Sample MCP-Style Gateway

This is a small FastAPI sample that teaches the pattern, not a production-complete platform.

## What it includes

- health endpoint
- token-based auth example
- simple role check
- read-only SQL stub
- safe file read stub

## Why this matters

This sample gives you something concrete to demo and extend.

## Run locally

```bash
cd mcp-gateway
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Example request

```bash
curl -H "Authorization: Bearer demo-analyst-token" http://127.0.0.1:8000/health
```

## Good next improvements

- JWT-based auth
- real database adapter
- structured audit logging to a datastore
- per-tool policy engine
- OpenTelemetry tracing
