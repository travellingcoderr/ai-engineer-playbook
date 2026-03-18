# Mortgage Bot Architecture

## Overview
`Mortgage Bot` is a mortgage-focused AI support and knowledge system. It mimics the advanced AI orchestration found in `EPM-CORE-API` but is built with a modern Python/React stack for scalability and ease of use.

## Technical Stack
- **Frontend**: React 18, Vite, TailwindCSS (for modern UI).
- **Backend**: FastAPI (Python 3.11).
- **Agent Orchestration**: LangGraph (ReAct pattern).
- **Database**: PostgreSQL with `pgvector` for both relational and vector data.
- **Task Queue**: Redis and `rq` for asynchronous document ingestion.
- **Infrastructure**: Docker Compose for localized enterprise-grade deployment.

## Key Logic Patterns
### 1. ReAct Agent
The agent uses a Reasoning + Acting loop. It can:
- Search the knowledge base for answers.
- Look up loan context (mocked for now).
- Analyze user issues and suggest resolutions before a ticket is even created.

### 2. Scalable Ingestion
When a user uploads a document, the API enqueues a job to Redis. A dedicated worker process picks up the job and performs:
- **Chunking**: Splitting the document into semantic parts.
- **Embedding**: Generating vector representations.
- **Upserting**: Saving to the `pgvector` store.

## Shared Core
`Mortgage Bot` leverages the global `packages/core` for standardized services:
- `LLMFactory`: Centralized model creation.
- `ToolFactory`: Shared tool definitions.
- `ObservabilityClient`: Holistic tracking of performance and token costs.
