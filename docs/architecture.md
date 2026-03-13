# Enterprise AI Architecture

Typical stack at large enterprises:

1. **Interface Layer**: API/UI (e.g., FastAPI, Next.js) where user interaction begins.
2. **Agent / Orchestration Layer** (`projects/multi_agent/`, `projects/research_agent/`): Handles complex workflows, planning, and task distribution among specialized AI agents.
3. **Retrieval Layer** (`projects/rag_system/`): Implements RAG (Retrieval-Augmented Generation) to ground LLMs with enterprise data using vector search.
4. **Tool Gateway Layer** (`mcp-gateway/`): An MCP-style centralized hub managing agent authentication, routing, and access to external capabilities securely.
5. **Guardrails Layer** (`projects/guardrails/`): Validates inputs/outputs, preventing prompt injections and enforcing compliance.
6. **Observability Layer** (`projects/observability/`): Tracks AI-specific telemetry like token usage and multi-agent execution paths.
7. **Cloud Infrastructure** (`infra/terraform/`): Base infrastructure, typically leveraging Azure OpenAI, container apps, and robust CI/CD (`tests/`).

## User Flow

```mermaid
flowchart TD
    User([User]) --> Interface[API / UI]
    Interface --> Agent[Agent / Orchestration]
    Agent --> Retrieval[(Retrieval / RAG)]
    Agent --> Tools[Tools Gateway / MCP]
    Tools -.-> DB[(Database / APIs)]
    Agent --> Guardrails[Guardrails Validation]
    Guardrails --> Output([Response sent to User])
    
    Observability[[Observability Layer]] -.-> Interface
    Observability -.-> Agent
    Observability -.-> Tools
    Observability -.-> Guardrails
    
    style Observability stroke-dasharray: 5 5
```
