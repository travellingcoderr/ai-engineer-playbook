# AI Engineer Playbook

A practical, GitHub-ready playbook for moving from cloud/backend engineering into production AI engineering.

This repo covers four things:
- the modern enterprise AI architecture stack
- a 30-day learning roadmap
- the fastest credible way to build an MCP gateway
- five portfolio projects that are strong enough to discuss in interviews

This repo is opinionated on purpose. It favors practical skills over hype.

## Who this is for

This playbook fits especially well if you already have a background in:
- cloud platforms like Azure or AWS
- backend APIs
- Terraform / IaC
- CI/CD
- security and access control

That is why this path is a good fit for you: you already have a lot of the platform skills that many AI engineers lack.

## Recommended reading order

1. [Architecture stack](docs/architecture/2025-ai-architecture-stack.md)
2. [30-day roadmap](docs/roadmap/30-day-roadmap.md)
3. [MCP gateway guide](docs/mcp/easiest-mcp-gateway.md)
4. [Interview projects](docs/projects/5-projects-for-interviews.md)
5. [Security checklist](docs/security/owasp-llm-and-guardrails.md)
6. [Platform comparison](docs/platforms/azure-foundry-vs-bedrock.md)
7. [Interview prep guide](docs/interview-prep/how-to-talk-about-your-projects.md)

## Suggested repo usage

Use this repo in one of two ways:

### Option A: knowledge repo
Keep this as a study repository with notes, diagrams, and project plans.

### Option B: living portfolio repo
Turn each project section into a real subproject over time. That gives you both learning notes and proof of execution.

## Repo structure

```text
ai-engineer-playbook/
├── README.md
├── docs/
│   ├── architecture/
│   │   └── 2025-ai-architecture-stack.md
│   ├── roadmap/
│   │   └── 30-day-roadmap.md
│   ├── mcp/
│   │   ├── easiest-mcp-gateway.md
│   │   ├── mcp-gateway-architecture.md
│   │   └── tool-access-control.md
│   ├── projects/
│   │   ├── 5-projects-for-interviews.md
│   │   └── project-scorecard-template.md
│   ├── security/
│   │   └── owasp-llm-and-guardrails.md
│   ├── platforms/
│   │   └── azure-foundry-vs-bedrock.md
│   └── interview-prep/
│       └── how-to-talk-about-your-projects.md
├── templates/
│   ├── project-readme-template.md
│   └── eval-dataset-template.json
├── mcp-gateway/
│   ├── README.md
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── models.py
│   │   └── tools.py
│   └── tests/
│       └── test_health.py
├── .github/
│   └── workflows/
│       └── ci.yml
└── scripts/
    └── bootstrap.sh
```

## What matters most in 2026

A strong AI engineer is usually strong in these six areas:
- model usage and prompting
- retrieval and data grounding
- agent orchestration
- tool integration
- security and access control
- evaluation and observability

The fastest path is not to learn everything. It is to build a few projects that force you to touch all six.

## Source notes

This repo intentionally leans on current primary sources where possible:
- MCP is an open protocol for connecting LLM apps to tools and data sources. citeturn584966search0
- Microsoft Foundry includes agent tooling, tracing, monitoring, evaluation, and a tool catalog with MCP server support. citeturn584966search1turn584966search9turn584966search21turn584966search17
- Amazon Bedrock Agents is a managed way to orchestrate models, APIs, data sources, and actions. citeturn584966search2turn584966search6turn584966search10turn584966search22
- OWASP maintains both the Top 10 for LLM applications and the broader GenAI security project. citeturn584966search3turn584966search11turn584966search23

## Next move

Start by reading the 30-day roadmap, then build the MCP gateway sample in this repo. That will give you a practical anchor instead of just theory.
