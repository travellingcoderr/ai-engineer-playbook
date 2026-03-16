# Research Agent Architecture: Autonomous LangGraph Loop

This document outlines the architecture of the **Research Agent**. The system uses a **LangGraph** driven finite state machine to autonomously navigate the web, scrape content, and compile comprehensive reports. 

## Why LangGraph?

Traditional LangChain chains are highly linear (Input -> LLM -> Output). However, true autonomous research requires cycles:
1. **Looping:** The agent must be able to search, read the results, and decide if it needs to search again based on missing information.
2. **State Management:** The agent must maintain memory of what URLs it has already visited and what facts it has already collected across dozens of tool calls.
3. **Control Flow:** We need to explicitly define when the agent is allowed to use tools and when it is forced to synthesize the final report.

LangGraph solves this by modeling the agent as a graph of nodes and edges, allowing for robust cyclic execution.

## Core Configuration

The agent shares the overarching `packages/core/config.py` with other projects in the repo (like the RAG system) for standard LLM initialization. It also defines its own specific application settings in `projects/research_agent/app/core/config.py`.

```env
# Shared Configuration (from root .env)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
TAVILY_API_KEY=tvly-...
```

## The Tool Factory

To maintain flexibility and follow the Abstract Factory pattern, the agent utilizes a `ToolFactory` (`app/tools/factory.py`).
- **Inputs:** A list of enabled tools defined in the agent's Pydantic config.
- **Outputs:** An array of instantiated `BaseTool` objects ready for injection into the LangGraph.

Currently supported tools:
1. **Tavily Search Tool (`app/tools/search.py`)**: An AI-native web search engine optimized for autonomous agents.
2. **Web Scrape Tool (`app/tools/scrape.py`)**: A BeautifulSoup implementation to extract raw text from target URLs.

## Flow of Execution (`app/agent/graph.py`)

1. **Trigger:** The FastAPI endpoint `/research` is called with a topic.
2. **Setup:** The `run()` method in `agent.py` initializes the LLM and the ToolFactory.
3. **Graph Execution Begins:**
   - **Researcher Node:** Analyzes the prompt and the current state history. If it needs data, it invokes tools.
   - **Tools Node:** Executes the requested searches or scrapes and passes the raw HTML/search results back to the Researcher. 
   - *(This loop continues until the Researcher asserts it has enough context).*
   - **Writer Node:** The Researcher passes control to the Writer. The Writer synthesizes the massive state history into a highly structured, heavily cited Markdown report.
4. **Return:** The final markdown string is returned to the user via the API.
