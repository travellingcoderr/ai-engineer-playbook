import contextvars
import math
import time
from typing import Any

from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel

from ..enums.observability import LogLevel, MetricUnit
from .observability import ObservabilityClient


MODEL_PRICING_PER_1K_TOKENS = {
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-4.1": {"input": 0.002, "output": 0.008},
    "gpt-4.1-mini": {"input": 0.0004, "output": 0.0016},
    "text-embedding-3-small": {"input": 0.00002, "output": 0.0},
    "text-embedding-3-large": {"input": 0.00013, "output": 0.0},
    "text-embedding-ada-002": {"input": 0.0001, "output": 0.0},
}

_instrumentation_context: contextvars.ContextVar[dict] = contextvars.ContextVar(
    "llm_instrumentation_context",
    default={},
)
_llm_record_sink = None


def set_llm_instrumentation_context(**kwargs: Any):
    current = dict(_instrumentation_context.get())
    current.update({key: value for key, value in kwargs.items() if value is not None})
    return _instrumentation_context.set(current)


def reset_llm_instrumentation_context(token) -> None:
    _instrumentation_context.reset(token)


def get_llm_instrumentation_context() -> dict:
    return dict(_instrumentation_context.get())


def set_llm_record_sink(sink) -> None:
    global _llm_record_sink
    _llm_record_sink = sink


class LLMInstrumentation:
    def __init__(
        self,
        service_name: str = "llm_runtime",
        provider: str | None = None,
        model_name: str | None = None,
        component: str = "unknown_component",
        operation: str = "unknown_operation",
    ):
        self.provider = provider or "unknown_provider"
        self.model_name = model_name or "unknown_model"
        self.component = component
        self.operation = operation
        self.obs_client = ObservabilityClient(service_name=service_name)

    def wrap(self, model: BaseChatModel) -> "InstrumentedChatModel":
        return InstrumentedChatModel(model=model, instrumentation=self)

    def wrap_embeddings(self, embeddings: Embeddings) -> "InstrumentedEmbeddings":
        return InstrumentedEmbeddings(embeddings=embeddings, instrumentation=self)

    def estimate_cost_usd(self, prompt_tokens: int, completion_tokens: int) -> float:
        pricing = MODEL_PRICING_PER_1K_TOKENS.get(self.model_name)
        if not pricing:
            return 0.0

        input_cost = (prompt_tokens / 1000) * pricing["input"]
        output_cost = (completion_tokens / 1000) * pricing["output"]
        return round(input_cost + output_cost, 6)

    def extract_usage(self, response: Any) -> dict[str, int]:
        usage_metadata = getattr(response, "usage_metadata", None) or {}
        response_metadata = getattr(response, "response_metadata", None) or {}
        token_usage = response_metadata.get("token_usage", {}) if isinstance(response_metadata, dict) else {}

        prompt_tokens = (
            usage_metadata.get("input_tokens")
            or token_usage.get("prompt_tokens")
            or response_metadata.get("input_tokens", 0)
            or 0
        )
        completion_tokens = (
            usage_metadata.get("output_tokens")
            or token_usage.get("completion_tokens")
            or response_metadata.get("output_tokens", 0)
            or 0
        )
        total_tokens = (
            usage_metadata.get("total_tokens")
            or token_usage.get("total_tokens")
            or response_metadata.get("total_tokens", 0)
            or prompt_tokens + completion_tokens
        )

        return {
            "prompt_tokens": int(prompt_tokens),
            "completion_tokens": int(completion_tokens),
            "total_tokens": int(total_tokens),
        }

    def record(self, latency_seconds: float, usage: dict[str, int], success: bool = True) -> None:
        prompt_tokens = usage["prompt_tokens"]
        completion_tokens = usage["completion_tokens"]
        total_tokens = usage["total_tokens"]
        cost_usd = self.estimate_cost_usd(prompt_tokens, completion_tokens)
        tags = {
            "provider": self.provider,
            "model": self.model_name,
            "component": self.component,
            "operation": self.operation,
            "success": str(success).lower(),
        }
        context = get_llm_instrumentation_context()
        payload = {
            "trace_id": context.get("trace_id", "unknown_trace"),
            "request_id": context.get("request_id", "unknown_request"),
            "feature": context.get("feature", self.component),
            "workflow_type": context.get("workflow_type", self.component),
            "step_name": context.get("step_name", self.operation),
            "model": self.model_name,
            "provider": self.provider,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost_usd": cost_usd,
            "latency_ms": round(latency_seconds * 1000, 3),
            "success": success,
        }

        self.obs_client.log(
            message=(
                f"LLM invocation measured for {self.component}.{self.operation} "
                f"provider={self.provider} model={self.model_name} "
                f"prompt_tokens={prompt_tokens} completion_tokens={completion_tokens} "
                f"total_tokens={total_tokens} cost_usd={cost_usd:.6f} latency_seconds={latency_seconds:.4f}"
            ),
            level=LogLevel.INFO if success else LogLevel.ERROR,
        )
        self.obs_client.metric("llm_prompt_tokens", prompt_tokens, unit=MetricUnit.COUNT, tags=tags)
        self.obs_client.metric("llm_completion_tokens", completion_tokens, unit=MetricUnit.COUNT, tags=tags)
        self.obs_client.metric("llm_total_tokens", total_tokens, unit=MetricUnit.COUNT, tags=tags)
        self.obs_client.metric("llm_cost_usd", cost_usd, unit=MetricUnit.USD, tags=tags)
        self.obs_client.metric("llm_latency_seconds", latency_seconds, unit=MetricUnit.SECONDS, tags=tags)
        if _llm_record_sink:
            try:
                _llm_record_sink(payload)
            except Exception:
                self.obs_client.log(
                    message="Failed to persist LLM instrumentation payload",
                    level=LogLevel.ERROR,
                )


class InstrumentedChatModel:
    def __init__(self, model: BaseChatModel, instrumentation: LLMInstrumentation):
        self.model = model
        self.instrumentation = instrumentation

    def bind_tools(self, tools: list[Any]) -> "InstrumentedChatModel":
        return InstrumentedChatModel(
            model=self.model.bind_tools(tools),
            instrumentation=self.instrumentation,
        )

    def invoke(self, input: Any, config: Any = None, **kwargs: Any) -> Any:
        start_time = time.time()
        try:
            response = self.model.invoke(input, config=config, **kwargs)
            latency_seconds = time.time() - start_time
            usage = self.instrumentation.extract_usage(response)
            self.instrumentation.record(latency_seconds=latency_seconds, usage=usage, success=True)
            return response
        except Exception:
            latency_seconds = time.time() - start_time
            self.instrumentation.record(
                latency_seconds=latency_seconds,
                usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                success=False,
            )
            raise

    def __getattr__(self, item: str) -> Any:
        return getattr(self.model, item)


class InstrumentedEmbeddings:
    def __init__(self, embeddings: Embeddings, instrumentation: LLMInstrumentation):
        self.embeddings = embeddings
        self.instrumentation = instrumentation

    def _estimate_tokens(self, texts: list[str]) -> int:
        try:
            import tiktoken

            encoding = tiktoken.get_encoding("cl100k_base")
            return sum(len(encoding.encode(text or "")) for text in texts)
        except Exception:
            return sum(max(1, math.ceil(len(text or "") / 4)) for text in texts)

    def embed_query(self, text: str) -> list[float]:
        start_time = time.time()
        try:
            result = self.embeddings.embed_query(text)
            latency_seconds = time.time() - start_time
            prompt_tokens = self._estimate_tokens([text])
            self.instrumentation.record(
                latency_seconds=latency_seconds,
                usage={
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": 0,
                    "total_tokens": prompt_tokens,
                },
                success=True,
            )
            return result
        except Exception:
            latency_seconds = time.time() - start_time
            self.instrumentation.record(
                latency_seconds=latency_seconds,
                usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                success=False,
            )
            raise

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        start_time = time.time()
        try:
            result = self.embeddings.embed_documents(texts)
            latency_seconds = time.time() - start_time
            prompt_tokens = self._estimate_tokens(texts)
            self.instrumentation.record(
                latency_seconds=latency_seconds,
                usage={
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": 0,
                    "total_tokens": prompt_tokens,
                },
                success=True,
            )
            return result
        except Exception:
            latency_seconds = time.time() - start_time
            self.instrumentation.record(
                latency_seconds=latency_seconds,
                usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                success=False,
            )
            raise

    def __getattr__(self, item: str) -> Any:
        return getattr(self.embeddings, item)
