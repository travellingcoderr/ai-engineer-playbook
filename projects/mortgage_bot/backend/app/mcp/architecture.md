# Mortgage Bot MCP Architecture

## Why MCP in this project

This mortgage bot is meant to teach how agent tooling works in a domain that feels realistic without getting unnecessarily complex.

The core idea is:

- LangGraph handles orchestration and the ReAct loop
- MCP-style tools provide structured access to loan, borrower, condition, and knowledge data
- RAG search handles fuzzy semantic lookup across documents
- Structured tools handle live or system-like data access

This separation is useful because mortgage support questions usually need both:

- policy or guideline lookup
- current operational loan context

Examples:

- "Why is LN-1002 stuck?"
- "What conditions are still open?"
- "What guideline might help resolve this issue?"

## What MCP means here

In a full MCP deployment, a dedicated MCP server would expose tools over the MCP protocol and the agent would connect to that external tool server.

For learning, this repository starts with an **in-process MCP-style package** under `app/mcp/`:

- one file per tool
- a simple `server.py` tool registry
- shared helper utilities in `tool_helpers.py`
- mock LOS-like data coming from the seeded `loans` table

This keeps the architecture understandable while preserving the mental model of MCP:

- the tools are separated from the agent
- the tools have stable interfaces
- the agent can reason about which tool to call
- the data source can later move behind a real external MCP server

## Tool boundaries

The current MCP package contains these mortgage-focused tools:

- `search_knowledge`
  - semantic lookup across mortgage knowledge documents
- `get_loan_details`
  - high-level loan state plus related ticket context
- `list_loan_conditions`
  - underwriting and processing conditions
- `get_borrower_profile`
  - borrower contact and profile metadata
- `get_milestone_history`
  - loan progression timeline

Each tool lives in its own file so the design stays easy to read and extend.

## Mock data strategy

The project seeds mock mortgage loans in `app/database.py`.

Those loan records include:

- core loan fields like borrower, status, milestone, and amount
- `additional_metadata.borrower_profile`
- `additional_metadata.conditions`
- `additional_metadata.milestone_history`

This lets the MCP-style tools return useful, mortgage-shaped data without needing a real LOS.

## How this fits with LangGraph and ReAct

The LangGraph agent binds the MCP-style tools and uses a ReAct loop:

1. Reason
   - the model reads the conversation and decides whether it needs a tool
2. Act
   - the tool node executes the requested tool
3. Observe
   - the tool output is added back into the message stream
4. Reason again
   - the model decides whether it has enough context to answer or whether it needs another tool

This loop is implemented in `app/langgraph/agent.py`.

## How MCP complements AI search

This project intentionally uses both structured tools and semantic retrieval.

Use RAG search when the agent needs:

- fuzzy similarity
- guideline lookup
- article retrieval
- semantic help content

Use MCP-style tools when the agent needs:

- exact loan state
- condition lists
- borrower details
- milestone history
- operational system context

Best pattern:

- user asks a mortgage support question
- agent decides whether it needs knowledge search, structured tools, or both
- tool results and search results are combined into a final answer

## Learning path

The recommended progression is:

1. Start with the current in-process MCP-style tools
2. Observe how LangGraph chooses tools in the ReAct loop
3. Add new mortgage tools one by one
4. Replace one local tool source with a real external system later
5. Eventually move the tool package behind a standalone MCP server if needed

## Future MCP server ideas

Good next mortgage-focused MCP servers or tool groups:

- LOS access
  - live loan details, milestones, borrower contacts
- document and underwriting system
  - missing documents, unresolved conditions
- guidelines or policy server
  - guideline search, exact section retrieval
- pricing or eligibility server
  - product fit, DTI/LTV checks
- ticketing or CRM server
  - create follow-up tasks, add notes, escalate issues
- compliance server
  - TRID timeline checks, disclosure audit flags

## Current integration summary

- `app/mcp/` holds mortgage-specific MCP-style tools
- `app/mcp/server.py` exposes the tool registry used by the LangGraph agent
- `app/langgraph/agent.py` binds those tools into the ReAct loop
- `app/database.py` seeds mock mortgage loan data
- `app/models/loan.py` defines the internal loan store used by the mock LOS tools

This gives a clear learning path:

- understand ReAct
- understand tool usage
- understand where structured system access fits beside knowledge search
- understand how an in-process tool layer can later become a real MCP server
