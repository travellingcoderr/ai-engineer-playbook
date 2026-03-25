# RAG System AKS Architecture

High-level flow:

```mermaid
flowchart LR
    U["Client"] --> ING["Ingress"]
    ING --> SVC["Service (ClusterIP)"]
    SVC --> POD["RAG System Pod"]
    POD --> KV["Azure Key Vault"]
    POD --> AOAI["OpenAI / Azure OpenAI"]
    POD --> VS["Vector Store"]
    ACR["Azure Container Registry"] --> AKS["AKS"]
    AKS --- ING
    AKS --- SVC
    AKS --- POD
```

Expected runtime dependencies:
- ingress for public access
- Key Vault for secrets
- external LLM provider
- vector store backend

Ingress:
- public traffic in

Egress:
- outbound calls to LLM, Key Vault, and vector store
