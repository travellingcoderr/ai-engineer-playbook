# AI Playbook Services Overview

This document summarizes the core microservices and infrastructure components available in the AI Engineer Playbook.

## 🏛 Core Services

| Service | Port | Folder | Description |
| :--- | :--- | :--- | :--- |
| **RAG System** | 8000 | `projects/rag_system` | Retrieval-Augmented Generation using Vector DBs. |
| **MCP Gateway** | 8001 | `projects/mcp_gateway` | Secure tool-calling hub for AI Agents. |
| **Observability** | 8002 | `projects/observability` | Token usage and TTFT telemetry. |
| **Research Agent** | 8003 | `projects/research_agent` | Single-agent info gathering system. |
| **Multi-Agent** | 8004 | `projects/multi_agent` | Orchestrated group of specialized agents. |
| **Guardrails** | 8005 | `projects/guardrails` | Input/Output security and compliance filtering. |
| **Resilient Gateway**| 8006 | `projects/resilient_gateway` | Multi-region LLM failover and load balancing. |
| **n8n Workflow** | 5678 | `projects/workflow_orchestrator`| Low-code visually orchestrated AI pipelines. |
| **AI Perf & Eval** | 8007 | `projects/ai_perf_eval` | Phase 4: Stress testing (k6) and Accuracy evals. |

## 🛠 Management Tools

- **Hub Dashboard**: `http://localhost:8080`
- **CLI Menu**: `./menu.py`
- **Direct Control**: `Makefile` targets (e.g., `make run-all`)
