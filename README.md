Welcome to the AI Engineer Playbook! This repository serves as a practical guide and template for implementing modern AI engineering patterns.

🚀 **[Open Hub Dashboard](http://localhost:8080)** - Command Center for all services.

Below is an expanded overview of the core patterns demonstrated in this playbook:

## 🏛 Core AI Patterns

### 1. RAG Systems (`projects/rag_system/`)
Retrieval-Augmented Generation (RAG) is essential for grounding LLMs in private or dynamic data. This pattern demonstrates document fetching, vector similarity search, and prompt-injected context to reduce hallucinations and improve accuracy.

### 2. AI Agents (`projects/research_agent/`, `projects/multi_agent/`)
Instead of simple prompt-response loops, agents can plan, use tools, and iterate to achieve a goal.
- **Research Agent**: A single-agent setup focused on gathering and synthesizing information.
- **Multi-Agent Orchestration**: Coordination of specialized agents working together to solve complex workflows.

### 3. MCP-style Gateways (`mcp-gateway/`, `projects/mcp_gateway/`)
Model Context Protocol (MCP) inspired API gateways. These act as centralized hubs managing authentication, tool exposing, model routing, and standardizing how applications access various capabilities seamlessly.

### 4. Guardrails (`projects/guardrails/`)
Safety and compliance are paramount. This pattern shows how to implement input/output filtering, PII redaction, tone-checking, and semantic validation to ensure the AI behaves within strictly defined boundaries.

### 5. Observability (`projects/observability/`)
Traditional APM isn't enough for AI. This segment showcases AI-specific telemetry: tracking prompt/completion token usage, monitoring latency to first token (TTFT), and tracing complex agent execution graphs.

### 6. Azure OpenAI Integration Structure
Demonstrates enterprise-grade setups for consuming Azure OpenAI services, highlighting best practices for deployment routing, region fallbacks, and secure access management.

### 7. n8n Workflow Examples
Examples of using low-code/no-code automation platforms like n8n to build visually orchestrated AI pipelines, integrating seamlessly with external APIs, databases, and AI models.

## 🛠 Infrastructure & Operations

### 8. Terraform Infra (`infra/terraform/`)
Infrastructure as Code (IaC) tailored for AI workloads. Includes scripts to provision necessary resources such as container apps, vector databases, and serverless functions repeatably and reliably.

### 9. CI/CD and Tests (`tests/`)
Testing non-deterministic AI outputs requires specialized strategies. This section covers prompt evaluations, deterministic unit tests for gateway logic (`mcp-gateway/tests/`), and integration testing to ensure reliability across your AI features.

---
*Explore the individual directories for code examples, boilerplate templates (`templates/`), and setup utilities (`scripts/`) to accelerate your AI engineering journey.*
