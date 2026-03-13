# 30-Day Learning Roadmap

This roadmap is built for someone with a backend/cloud background who wants to become credible in AI engineering fast.

The goal is not to master everything in 30 days. The goal is to build enough depth to discuss real systems confidently.

## Week 1 — Foundations that actually matter

### Day 1
- Learn the difference between prompting, RAG, agents, and fine-tuning.
- Write down one sentence for each in your own words.

### Day 2
- Learn embeddings, chunking, vector search, and reranking.
- Build a tiny script that embeds text and retrieves the most similar chunk.

### Day 3
- Build a minimal RAG app with a local document set.
- Make it answer with citations.

### Day 4
- Improve the RAG app:
  - better chunking
  - metadata filters
  - basic evaluation set

### Day 5
- Study structured outputs and tool calling.
- Make the model return JSON reliably.

### Day 6
- Learn when not to use an agent.
- Compare single-shot prompting vs tool-based workflows.

### Day 7
- Write a short design note:
  - what failed in your RAG app
  - what improved it
  - where hallucinations still happen

## Week 2 — Agents and workflow orchestration

### Day 8
- Learn agent basics:
  - planning
  - tool use
  - loop control
  - state

### Day 9
- Build a 2-tool agent:
  - web search stub
  - calculator or local document search

### Day 10
- Add memory/state handling.
- Keep logs of user input, tool calls, and final answer.

### Day 11
- Learn graph-based orchestration.
- Build a tiny workflow with explicit nodes:
  - classify request
  - choose tool
  - produce answer

### Day 12
- Add failure handling and retries.
- Make tool errors visible in logs.

### Day 13
- Learn streaming responses and why they matter in UX.

### Day 14
- Write a project README explaining:
  - problem
  - architecture
  - tradeoffs
  - future improvements

## Week 3 — MCP and secure tool access

### Day 15
- Read what MCP is and what problem it solves. MCP is defined by its official specification as an open protocol for integrating LLM apps with external tools and data sources. citeturn584966search0

### Day 16
- Build your first simple MCP-style tool gateway.
- Expose two safe tools only:
  - read-only SQL query
  - repository file search

### Day 17
- Add authentication.
- Add role checks per tool.

### Day 18
- Add audit logging:
  - who called what
  - when
  - with what arguments
  - what result status happened

### Day 19
- Add input validation:
  - no destructive SQL
  - path allowlist for files

### Day 20
- Add rate limiting and basic abuse protection.

### Day 21
- Write an architecture note for your gateway.

## Week 4 — Evals, observability, and guardrails

### Day 22
- Learn why demos lie and evals matter.
- Create a tiny benchmark dataset of 20 questions.

### Day 23
- Score your system for:
  - correctness
  - citation quality
  - latency
  - cost

### Day 24
- Add prompt injection test cases.
- OWASP identifies prompt injection as a top LLM application risk. citeturn584966search3turn584966search11

### Day 25
- Add secure output handling rules.
- OWASP also calls out insecure output handling as a major risk. citeturn584966search3

### Day 26
- Add refusal or escalation paths for high-risk actions.

### Day 27
- Add tracing.
- Microsoft Foundry highlights tracing and evaluation support for agentic systems. citeturn584966search1turn584966search5

### Day 28
- Build a one-page dashboard or log summary.

### Day 29
- Prepare interview stories for 3 projects.

### Day 30
- Publish polished READMEs and architecture diagrams to GitHub.

## What you should have by the end

By day 30, you should be able to show:
- one RAG app
- one tool-using agent
- one secure MCP-style gateway
- one evaluation dataset and scoring loop
- one guardrails/security checklist

That is enough to start sounding like someone who has built systems instead of just watched tutorials.
