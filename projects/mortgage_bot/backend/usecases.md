# Mortgage Bot Use Cases

## Purpose

This document explains which orchestration style is used for which type of problem in the mortgage bot backend.

The project intentionally includes multiple patterns so you can learn where each one fits:

- plain RAG / knowledge retrieval
- MCP-style structured tools
- LangGraph ReAct
- CrewAI multi-agent collaboration
- RQ worker processing for background jobs

## 1. Plain RAG / Knowledge Retrieval

Use this when the problem is mainly about finding relevant text or guidance.

Typical use cases:

- searching mortgage guidelines
- searching uploaded policy documents
- finding similar written support content

What it is good at:

- semantic similarity
- fuzzy document retrieval
- supporting references

What it is not good at by itself:

- exact loan state
- operational system context
- multi-step reasoning with tools

Current examples:

- `RAGService.search(...)`
- knowledge search result building in `app/api/knowledge.py`

## 2. MCP-Style Tools

Use MCP-style tools when the problem needs structured operational data, not just document similarity.

Typical use cases:

- get loan details for `LN-1002`
- list open conditions
- get milestone history
- get borrower profile

What it is good at:

- exact values
- workflow context
- stateful mortgage data

Current examples:

- `app/mcp/get_loan_details.py`
- `app/mcp/list_loan_conditions.py`
- `app/mcp/get_milestone_history.py`
- `app/mcp/get_borrower_profile.py`

## 3. LangGraph ReAct

Use LangGraph when one agent needs to reason about the problem, decide which tools to call, observe the results, and iterate.

Typical use cases:

- instant help on a ticket before creating it
- mortgage knowledge search with tool calling
- explaining why a loan is stuck

What it is good at:

- explicit reason/act/observe loops
- transparent tool orchestration
- deterministic workflow control

Current examples:

- `app/langgraph/agent.py`
- `GET /api/knowledge/agent-search`
- `GET /api/knowledge/agent-assist`

Example query:

- `Why is LN-1002 stuck and what should I do next?`

Likely flow:

1. reason about the user question
2. call `get_loan_details`
3. call `list_loan_conditions`
4. possibly call `search_knowledge`
5. synthesize the final answer

## 4. CrewAI

Use CrewAI when you want a team of role-based agents to collaborate on the same mortgage support problem.

Typical use cases:

- mortgage ticket triage
- issue summarization
- operational review plus guideline review plus final resolution

What it is good at:

- specialization by role
- multi-agent task handoff
- comparing collaborative agent behavior with single-agent ReAct

Current examples:

- `app/crewai/agents.py`
- `app/crewai/tasks.py`
- `app/crewai/crew.py`
- `GET /api/crew/triage`

Current crew roles:

- Mortgage Intake Analyst
- Mortgage Loan Ops Specialist
- Mortgage Guidelines Researcher
- Mortgage Resolution Writer

## 5. RQ Worker Processing

Use RQ workers when the task should happen asynchronously and does not need to block the API request.

Typical use cases:

- document ingestion
- PDF extraction
- chunking and vector storage
- future background summarization or indexing jobs

What it is good at:

- long-running background work
- separating user request latency from processing time
- retriable job execution

Current examples:

- `app/api/knowledge.py` queues ingestion jobs
- `worker/tasks/ingestion.py` processes the jobs

## 6. Worker Job Tracking

To make queued background work visible, the backend stores worker job state in a database table.

Tracked states:

- `queued`
- `processing`
- `completed`
- `failed`

Tracked fields:

- job identifier
- queue name
- task name
- related document id
- payload
- error message
- enqueue/start/complete timestamps

Current examples:

- `app/models/worker_job.py`
- `app/data/worker_job_repository.py`
- `GET /api/jobs`
- `GET /api/jobs/{job_id}`

## 7. LLM Instrumentation

The backend also stores model usage metrics for both chat and embedding calls.

Tracked metrics:

- trace id
- request id
- feature
- workflow type
- step name
- model
- provider
- prompt tokens
- completion tokens
- total tokens
- cost in USD
- latency in milliseconds
- success/failure

This is used to compare:

- LangGraph cost
- CrewAI cost
- search-time embedding cost
- ingestion-time embedding cost

Current examples:

- `app/models/llm_invocation.py`
- `GET /api/instrumentation/summary`
- `GET /api/instrumentation/events`

## Quick Guidance

Use:

- RAG when you mainly need document similarity
- MCP tools when you need exact mortgage system data
- LangGraph when one agent should reason and call tools iteratively
- CrewAI when you want multiple specialists collaborating
- RQ when the work should happen in the background

This is the current teaching shape of the mortgage bot:

- mortgage domain context through mock loan data
- structured tool access through MCP-style tools
- single-agent orchestration through LangGraph
- multi-agent orchestration through CrewAI
- asynchronous processing through RQ
- instrumentation for cost, token, and latency visibility
