# How to Talk About Your AI Projects in Interviews

A good project is not enough. You need a clean story.

## The format

For each project, explain it in this order:

1. Problem
2. Why a basic chatbot was not enough
3. Architecture
4. Key tradeoffs
5. Security / guardrails
6. Evaluation approach
7. What failed and how you improved it

## Example framing

### RAG assistant
- Problem: internal docs were hard to search accurately.
- Architecture: ingestion pipeline, embeddings, vector search, answer generation with citations.
- Tradeoff: better chunking improved retrieval but increased ingestion complexity.
- Evals: measured answer correctness and citation relevance on a small benchmark set.

### MCP gateway
- Problem: agents needed controlled access to enterprise tools.
- Architecture: FastAPI gateway, tool registry, auth, validators, audit logs.
- Tradeoff: narrow tools reduced flexibility but improved safety and debuggability.
- Security: default-deny policy, read-only tools first, input validation.

## Questions you should be ready for

- Why did you choose an agent instead of a workflow?
- Where can this system hallucinate?
- How do you prevent prompt injection?
- How would you evaluate it in production?
- How do you control cost and latency?
- How would you restrict tool access by user role?

## The mistake to avoid

Do not present your project like a feature list.

Present it like an engineering problem you solved.
