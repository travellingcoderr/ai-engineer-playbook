# Deep Dive: AI Engineering Patterns

This document explores how the various AI patterns are currently implemented in the repository, and maps them directly to the `Enterprise AI Architecture` flow. 

## 1. Tool Gateway Layer (`mcp-gateway/`)
*The most comprehensive component in this repository.*

The gateway acts as an API integration layer implementing a streamlined version of the Model Context Protocol (MCP).
- **Structure**: A FastAPI application (`mcp-gateway/app/main.py`) handles incoming requests to `/tools/invoke`.
- **Authentication**: Uses Bearer tokens (`mcp-gateway/app/auth.py`) that map to specific roles (`analyst`, `engineer`, `admin`).
- **Role-Based Tools**: Driven by `mcp-gateway/app/tools.py`, which restricts what tools each role can execute:
  - `health_check`: Available to all.
  - `read_repo_file`: Available to `engineer` and `admin`. Ensures files are only read within permitted directories to prevent traversal attacks.
  - `query_readonly_sql`: Available to `analyst` and `admin`. Includes basic safeguards refusing `UPDATE`, `DELETE`, etc., forcing only `SELECT` queries.

This creates a secure sandbox where AI Agents can only affect safe domains.

## 2. Agent / Orchestration Layer (`projects/multi_agent/`, `projects/research_agent/`)
*Currently established as foundational concepts.*

- **Single Agent (`research_agent/agent.py`)**: A stubbed `run(topic)` function designed to house a dedicated prompt-response loop specialized for deep-dive research tasks.
- **Multi-Agent Orchestrator (`multi_agent/workflow.py`)**: Demonstrates a "planner-worker" relationship. A `planner()` breaks a goal into tasks (e.g., `["research", "write"]`), which would then be dispatched to specialized agents (like the research agent above).

## 3. Retrieval Layer (`projects/rag_system/`)
*Currently established as a structural API concept.*

- Implemented as a FastAPI app (`projects/rag_system/app/main.py`) with an `/ask` endpoint.
- In a production RAG system, this is where document chunking, embedding generation (e.g., via OpenAI embeddings model), and vector similarity search (e.g., Pinecone, Qdrant) occur to inject relevant context before querying an LLM.

## 4. Guardrails Layer (`projects/guardrails/`)
*Essential for enterprise compliance.*

- `projects/guardrails/filter.py` contains a `detect_prompt_injection` function identifying malicious phrases like *"ignore previous instructions"* or *"reveal system prompt"*.
- In practice, this layer sits between the user interface and the orchestration layer to block adversarial inputs before they consume AI compute costs.

## 5. Observability Layer (`projects/observability/`)
*Essential for evaluating AI responses.*

- `projects/observability/logger.py` demonstrates logging `{prompt, response, timestamp}`.
- Further expansion typically includes telemetry traces for Time to First Token (TTFT), token counts, cost tracking, and tracking multi-agent execution paths using tools like Langfuse or Arize Phoenix.

---

### How it all connects to your user flow:

When a User submits a request via the **Interface Layer**, the **Agent** takes the request and plans the steps. 
It might first query the **Retrieval Layer (RAG)** for enterprise context. 
If it needs to execute a query against a database or read a GitHub repo file, it asks the **Tool Gateway (MCP)**, which authenticates the Agent's role and ensures it is authorized.
Throughout the process, the **Guardrails Layer** intercepts and validates the Agent outputs to ensure it doesn't return PII or execute malicious code, and the **Observability Layer** logs every interaction trace for debugging. 
