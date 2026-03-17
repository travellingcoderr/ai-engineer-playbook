# Resilient Gateway Architecture

The Resilient Gateway acts as a smart proxy for LLM requests, providing enterprise-grade reliability through multi-provider routing and automated failover.

## Core Components

### 1. Unified API
Exposes an OpenAI-compatible interface (e.g., `/v1/complete`) to downstream services. This decouples individual microservices from specific provider quirks.

### 2. Resilient Router
The heart of the service. It manages a list of prioritized providers and executes a "Retry-with-Next" strategy if a provider fails or returns a rate limit (429).

### 3. Provider Adapters
Modular plugins for different LLM backends:
- **MockAzureProvider**: Simulates regional failures for zero-cost testing.
- **AzureOpenAIProvider**: Handles deployment-to-model mapping and Managed Identity auth.
- **OpenAIProvider**: Direct integration with OpenAI.

### 4. Observability & Auditing
- **Audit Logs**: Every request is logged with its duration and status.
- **Metrics**: Tracks latency and failure rates per provider to inform routing decisions.

## Failover Flow
1. Service sends request for `gpt-4o`.
2. Router picks **Primary Provider** (e.g., Azure East US).
3. Primary Provider fails with 429.
4. Router catches exception and immediately tries **Secondary Provider** (e.g., Azure West Europe).
5. Router returns response to Service, hiding the complexity of the failure.
