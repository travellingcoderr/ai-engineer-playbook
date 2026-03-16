# Multi-Agent Services Sandbox

The Multi-Agent orchestration is encapsulated seamlessly behind a single FastAPI container on port `8004`.

| Service | Port / Location | Responsibilities |
|---------|-----------------|------------------|
| **Multi-Agent Orchestrator** | `8004` (Docker) | The `FastAPI` instance exposing the synchronous `/team/run` trigger API. |
| **LangGraph Core** | Internal Module | The `StateGraph` object managing the message DAG tracking the state execution. |
| **Supervisor Node** | Internal LLM Router | Evaluates context and explicitly routes control to a subordinate via `next` key string. |
| **Researcher Node** | Internal Worker | LangChain Agent armed with live Web-Search execution tools. |
| **Coder Node** | Internal Worker | Standard LangChain text-generator executing developer constraints. |

## Booting

The service is fully orchestrated through the global tools:
```bash
# Using the root Menu UI
./menu.py (Select Option 5)

# Using raw Make
make run-docker-multi-agent
```
