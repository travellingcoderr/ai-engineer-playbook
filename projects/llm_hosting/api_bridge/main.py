import json
import logging
import os
import time
from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, Security, status
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import StreamingResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from pydantic import BaseModel, Field, ConfigDict

class Settings(BaseModel):
    api_key: str = Field(default=os.getenv("API_KEY", "change-me"))
    llm_provider: str = Field(default=os.getenv("LLM_PROVIDER", "ollama").lower())
    ollama_url: str = Field(default=os.getenv("OLLAMA_URL", "http://ollama:11434"))
    openai_api_key: str | None = Field(default=os.getenv("OPENAI_API_KEY"))
    openai_base_url: str = Field(default=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    default_model: str = Field(default=os.getenv("DEFAULT_MODEL", "llama3.2:3b"))
    request_timeout_seconds: float = Field(
        default=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "300"))
    )
    rate_limit_per_minute: int = Field(default=int(os.getenv("RATE_LIMIT_PER_MINUTE", "5")))


settings = Settings()
API_KEY_NAME = "X-API-KEY"

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("api-bridge")


class ChatMessage(BaseModel):
    role: str
    content: str | list[dict] | None


class ChatCompletionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str | None = None
    messages: list[ChatMessage]
    stream: bool = False
    temperature: float | None = None
    max_tokens: int | None = None


limiter = Limiter(key_func=get_remote_address)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    timeout = httpx.Timeout(settings.request_timeout_seconds)
    async with httpx.AsyncClient(timeout=timeout) as client:
        app.state.http_client = client
        yield


app = FastAPI(title="LLM API Bridge", version="0.1.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


async def get_api_key(header_key: str | None = Security(api_key_header)) -> str:
    # This key protects your own gateway. It is not the same as a model-provider key.
    if header_key == settings.api_key:
        return header_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate API key",
    )


def _upstream_chat_url() -> str:
    if settings.llm_provider == "openai":
        return f"{settings.openai_base_url.rstrip('/')}/chat/completions"
    return f"{settings.ollama_url.rstrip('/')}/v1/chat/completions"


def _upstream_headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise HTTPException(
                status_code=500,
                detail="OPENAI_API_KEY is required when LLM_PROVIDER=openai",
            )
        headers["Authorization"] = f"Bearer {settings.openai_api_key}"
    return headers


def _upstream_tags(model: str, request: Request, started_at: float) -> dict:
    return {
        "client_ip": request.client.host if request.client else "unknown",
        "latency_ms": int((time.time() - started_at) * 1000),
        "model": model,
    }


@app.get("/")
async def root():
    return {
        "service": "llm-api-bridge",
        "status": "ok",
        "routes": ["/health", "/ready", "/v1/chat/completions"],
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/ready")
async def readiness_check(_: str = Depends(get_api_key)):
    try:
        # Use a lightweight provider-specific readiness check so callers know
        # whether the configured upstream is reachable before sending prompts.
        if settings.llm_provider == "openai":
            response = await app.state.http_client.get(
                f"{settings.openai_base_url.rstrip('/')}/models",
                headers=_upstream_headers(),
            )
        else:
            response = await app.state.http_client.get(f"{settings.ollama_url.rstrip('/')}/api/tags")
        response.raise_for_status()
        return {
            "status": "ready",
            "provider": settings.llm_provider,
            "details": response.json(),
        }
    except httpx.HTTPError as exc:
        logger.exception("Inference readiness check failed")
        raise HTTPException(status_code=503, detail=f"Inference server unavailable: {exc}") from exc


async def _stream_upstream_response(payload: dict):
    async with app.state.http_client.stream(
        "POST",
        _upstream_chat_url(),
        json=payload,
        headers=_upstream_headers(),
    ) as response:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text
            logger.error("Upstream streaming request failed: %s", detail)
            raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc

        async for chunk in response.aiter_bytes():
            if chunk:
                yield chunk


@app.post("/v1/chat/completions")
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat_completions(
    request: Request,
    payload: ChatCompletionRequest,
    _: str = Depends(get_api_key),
):
    started_at = time.time()
    body = payload.model_dump(exclude_none=True)
    body["model"] = body.get("model") or settings.default_model

    logger.info(
        "Handling chat completion request: %s",
        json.dumps(
            {
                "client_ip": request.client.host if request.client else "unknown",
                "provider": settings.llm_provider,
                "model": body["model"],
                "message_count": len(body["messages"]),
                "stream": body.get("stream", False),
            }
        ),
    )

    if body.get("stream"):
        return StreamingResponse(
            _stream_upstream_response(body),
            media_type="text/event-stream",
        )

    try:
        # The bridge forwards an OpenAI-style payload to whichever provider is configured.
        response = await app.state.http_client.post(
            _upstream_chat_url(),
            json=body,
            headers=_upstream_headers(),
        )
        response.raise_for_status()
        logger.info("Upstream chat completed: %s", json.dumps(_upstream_tags(body["model"], request, started_at)))
        return response.json()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text
        logger.error("Upstream request failed: %s", detail)
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc
    except httpx.RequestError as exc:
        logger.exception("Failed to reach inference server")
        raise HTTPException(status_code=503, detail="Inference server unavailable") from exc

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
