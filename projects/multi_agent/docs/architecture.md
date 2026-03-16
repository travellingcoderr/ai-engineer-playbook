# Multi-Agent Orchestrator Architecture

The `multi_agent` system relies on **LangGraph** to replace static code pipelines with a dynamic, cyclical group of specialized agents.

## Core LangGraph Flow

1. **TeamState (`app/agent/state.py`)**: The global memory of the team. Holds the unified Message History and the target routing `next` step.
2. **Supervisor Node (`app/agent/nodes/supervisor.py`)**: The manager. It evaluates the state memory and uses LLM structured outputs to explicitly route to the correct worker, or conclude with `FINISH`.
3. **Researcher Node (`app/agent/nodes/researcher.py`)**: A ReAct-based node equipped with `DuckDuckGo` / `Tavily` for external, autonomous fact-gathering.
4. **Coder Node (`app/agent/nodes/coder.py`)**: A pure LLM node embedded with strict Python formatting prompts. It generates code based strictly on the Researcher's context.

## Standardization & Patterns

Inheriting the success of the RAG System, this app implements:
- **Dependency Injection**: Leverages `packages.core.config` exclusively. No duplicated `.env` parsing algorithms.
- **Factory Ecosystem**: `LLMFactory` and `ToolFactory` abstract away the underlying provider details so the Worker Nodes focus purely on business logic.
