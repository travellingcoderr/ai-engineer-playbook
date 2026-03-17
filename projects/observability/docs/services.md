# Observability API Services

This document outlines the ingestion endpoints for the Observability Collector.

## 1. POST `/ingest/log`
- **Description**: Ingests a structured JSON log entry.
- **Request Body** (`LogEntry`):
  ```json
  {
    "service": "rag_system",
    "level": "ERROR",
    "message": "Failed to connect to vector database",
    "trace_id": "trace-12345",
    "metadata": {"db_type": "chroma", "retry": 3}
  }
  ```

## 2. POST `/ingest/metric`
- **Description**: Ingests a telemetry metric.
- **Request Body** (`MetricEntry`):
  ```json
  {
    "service": "mcp_gateway",
    "name": "llm_tokens",
    "value": 245,
    "unit": "tokens",
    "labels": {"model": "gpt-4o", "user": "corp-user-1"}
  }
  ```

## 3. POST `/ingest/trace`
- **Description**: Records a distributed trace span.
- **Request Body** (`TraceSpan`):
  ```json
  {
    "service": "research_agent",
    "operation": "web_scrape",
    "trace_id": "abc-789",
    "span_id": "span-456",
    "start_time": "2026-03-16T17:00:00Z",
    "end_time": "2026-03-16T17:00:05Z"
  }
  ```

## 4. GET `/health`
- **Description**: Returns the collector status and the active ingestion strategy.

---

## Third-Party Integration
To see these logs in "Corporate" platforms:
1. **LangSmith**: Set environment variables `LANGCHAIN_TRACING_V2=true` and `LANGCHAIN_API_KEY`.
2. **Arize Phoenix**: Run a local Phoenix container and point your collector to it.
3. **Datadog**: Install the Datadog tailer to read from `observability.log`.
