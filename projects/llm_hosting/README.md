# LLM Hosting Setup (Free Starter)

This project provides a minimal self-hosted LLM stack using **Ollama** and a **FastAPI** bridge. The bridge adds:

- API key auth
- rate limiting
- request logging
- health and readiness endpoints
- an OpenAI-compatible `/v1/chat/completions` route
- optional public exposure later through Cloudflare Tunnel

The bridge can now route requests to either:

- `ollama` for local open-weight models
- `openai` for OpenAI-hosted models

## Quick Start

### 1. Requirements
- Docker & Docker Compose
- (Recommended for Mac) [Ollama App](https://ollama.com/download) for GPU acceleration.

### 2. Configure Environment
Create a `.env` file in this directory or use the defaults in `docker-compose.yml`.

```bash
API_KEY=my-secure-token
LLM_PROVIDER=ollama
DEFAULT_MODEL=llama3.2:3b
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
RATE_LIMIT_PER_MINUTE=5
REQUEST_TIMEOUT_SECONDS=300
```

Generate a random `API_KEY` locally:
```bash
openssl rand -hex 32
```

Use that output in your `.env`:
```bash
API_KEY=<paste-generated-value>
```

What each key means:

- `API_KEY`: your own gateway secret for clients calling this bridge
- `LLM_PROVIDER`: `ollama` or `openai`
- `DEFAULT_MODEL`: default chat model if the request does not specify one
- `OPENAI_API_KEY`: only required when `LLM_PROVIDER=openai`
- `OPENAI_BASE_URL`: leave as default unless using a compatible proxy

### 3. Start the Stack
```bash
docker-compose up -d
```

If you are using the native Ollama app on your Mac, change `OLLAMA_URL` for the `api-bridge` service to `http://host.docker.internal:11434` to use local Metal acceleration instead of the containerized Ollama service.

If you want to use OpenAI instead of Ollama:
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
DEFAULT_MODEL=gpt-4o-mini
```

### 4. Pull a Model
If using the containerized Ollama:
```bash
docker exec -it llm_hosting-ollama-1 ollama pull llama3.1
```

---
### 5. Verify Readiness
Health:
```bash
curl http://localhost:8000/health
```

Readiness:
```bash
curl -H "X-API-KEY: my-secure-token" http://localhost:8000/ready
```

The readiness response includes the configured provider so you can confirm whether the bridge is targeting `ollama` or `openai`.

### 6. Call The Chat API
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "X-API-KEY: my-secure-token" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:3b",
    "messages": [
      {"role": "system", "content": "You are a concise assistant."},
      {"role": "user", "content": "Explain what an embedding is in one paragraph."}
    ]
  }'
```

## API Endpoints

- `GET /` basic service info
- `GET /health` liveness check
- `GET /ready` authenticated readiness check against Ollama
- `POST /v1/chat/completions` OpenAI-style chat route

## Fine-Tuning Starter

A beginner-friendly LoRA fine-tuning starter project is included here:

- [finetuning/README.md](/Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/llm_hosting/finetuning/README.md)
- [fine-tuning-notes.md](/Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/llm_hosting/fine-tuning-notes.md)

Use it if you want to learn how to train an adapter and then deploy that tuned model with Ollama or vLLM.

## Hosting For Free (Public API)

To expose this API to the internet for free without opening router ports or paying for a static IP, use **Cloudflare Tunnel (Cloudflared)**.

### 1. Install Cloudflared
```bash
brew install cloudflare/cloudflare/cloudflared
```

### 2. Authenticate
```bash
cloudflared tunnel login
```

### 3. Create a Tunnel
```bash
cloudflared tunnel create llm-hosting
```

### 4. Route to a Subdomain
```bash
# Replace <tunnel-id> and <your-domain.com>
cloudflared tunnel route dns llm-hosting api.yourdomain.com
```

### 5. Run the Tunnel
Create a `config.yml` for cloudflared:
```yaml
tunnel: <tunnel-id>
credentials-file: /Users/<user>/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: api.yourdomain.com
    service: http://localhost:8000
  - service: http_status:404
```
Then run:
```bash
cloudflared tunnel run llm-hosting
```

---

## Features Included

### API Key Authentication
Requests must include the header `X-API-KEY: your-token`.
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
     -H "X-API-KEY: my-secure-token" \
     -H "Content-Type: application/json" \
     -d '{"model": "llama3.1", "messages": [{"role": "user", "content": "hello"}]}'
```

### Rate Limiting
Defaults to `5 requests per minute` and is configurable through `RATE_LIMIT_PER_MINUTE`.

### Logging
Requests and upstream latency are logged to stdout in the API container.

### OpenAI-Compatible API
The bridge proxies to the `/v1/chat/completions` endpoint, allowing you to use standard OpenAI SDKs by changing the `base_url`.

### Streaming Support
If the client sends `"stream": true`, the bridge passes through the streaming response from Ollama.

### Provider Switching
Use `LLM_PROVIDER=ollama` for local open-weight hosting, or `LLM_PROVIDER=openai` if you want the bridge to send requests to OpenAI instead.
