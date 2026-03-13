
# AI Engineer Playbook (Phase 2)

This repository demonstrates practical, production-style AI engineering patterns.

## Projects Included

1. **Enterprise RAG System**
2. **AI Research Agent**
3. **MCP Tool Gateway**
4. **AI Security Guardrails**
5. **AI Observability Dashboard**

Each project is structured as a standalone service with minimal dependencies so it can run locally.

## Repo Structure

```
ai-engineer-playbook
│
├── projects
│   ├── rag-system
│   ├── research-agent
│   ├── mcp-gateway
│   ├── guardrails
│   └── observability
│
├── docs
│   ├── architecture.md
│   ├── roadmap.md
│   └── security.md
│
└── .github/workflows
    └── ci.yml
```

## Run a Sample Project

Example:

```
cd projects/mcp-gateway
pip install -r requirements.txt
python main.py
```

Then open:

http://localhost:8000/docs
