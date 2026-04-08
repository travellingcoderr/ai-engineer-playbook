# Azure AI Mental Model For This Project

This document is the clean mental model for this repo.

If you remember only one thing, remember this:

- Microsoft Foundry is the platform and management layer.
- Azure OpenAI is the model inference layer.
- Azure AI Document Intelligence is the document extraction layer.
- Azure AI Search is the retrieval layer.
- MCP is the tool bridge layer.
- Your application code is the orchestration layer.

## 1. The Core Difference

### Microsoft Foundry

Microsoft Foundry is the umbrella platform for building and operating AI apps and agents on Azure.

It gives you:

- projects
- agent definitions and versions
- model catalog and deployment experience
- monitoring, governance, identity, and policy controls
- a place to connect tools and resources

Foundry is not "the model" itself.
Foundry is the platform that helps you organize, govern, deploy, and operate AI systems.

### Azure OpenAI

Azure OpenAI is the model-serving service.

It gives you:

- GPT models
- embeddings models
- image/audio models depending on deployment
- runtime inference endpoints like chat, responses, embeddings

When your app wants the LLM to think, call tools, or generate text, this is usually the actual runtime doing the work.

In this repo today, the runtime inference path is the direct Azure OpenAI endpoint, not the project-scoped Foundry runtime path.

### Azure AI Document Intelligence

Document Intelligence is for reading documents.

It does:

- OCR
- layout extraction
- tables
- structured fields
- converting PDFs into machine-usable text/Markdown

It is not your LLM.
It does not replace Azure OpenAI.
It prepares documents so the LLM and retrieval system can use them.

### Azure AI Search

Azure AI Search is the retrieval database and ranking layer.

It stores and queries:

- indexed document chunks
- vectors / embeddings
- keyword results
- semantic ranking results

It is not the model.
It is not the document parser.
It is the searchable knowledge base.

### MCP

MCP is not an Azure model or storage service.
It is a protocol for tool execution.

It lets your model call tools like:

- Slack
- Maps
- custom Python tools
- internal business APIs

In this repo, MCP is how the model reaches operational tools.

## 2. The Correct Stack For This Repo

The intended end-to-end flow is:

1. Event Hub receives an external disruption event.
2. Your app consumes that event.
3. The orchestrator asks the LLM what to do.
4. The LLM can call tools.
5. Some tools query Azure AI Search for policy documents.
6. Some tools call MCP servers for operational actions.
7. The app returns a final summary.
8. Optional guardrails evaluate the final answer.

The document ingestion flow is separate:

1. A PDF or document is sent to Document Intelligence.
2. Document Intelligence extracts structured content.
3. That content is chunked and embedded.
4. The chunks are pushed into Azure AI Search.
5. Later, the runtime can retrieve those chunks during incident handling.

This separation matters:

- Document Intelligence is offline or pre-processing.
- Search is retrieval storage.
- Azure OpenAI is runtime reasoning.
- Foundry is the platform around all of it.

## 3. How This Repo Maps To The Azure Stack

### Runtime Entry

[app/main.py](/Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/sentinel-ai-hub/app/main.py)

- consumes Event Hub messages
- starts the orchestrator
- passes incident events into the AI workflow

### Foundry Project Management

[app/core/foundry_client.py](/Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/sentinel-ai-hub/app/core/foundry_client.py)

- creates `AIProjectClient`
- manages Foundry project access
- creates the runtime OpenAI client
- in this repo, prefers direct `AZURE_OPENAI_ENDPOINT` for inference

Important:
Foundry is still used here for project/agent registry operations, even when direct Azure OpenAI is used for model inference.

### Orchestration

[app/agents/orchestrator_agent.py](/Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/sentinel-ai-hub/app/agents/orchestrator_agent.py)

- coordinates the workflow
- builds the prompt
- calls the Responses API
- handles tool calls
- sends tool outputs back
- applies safety evaluation at the end

This file is the brain of the app.

### Agent Definitions

[app/agents/policy_expert_agent.py](/Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/sentinel-ai-hub/app/agents/policy_expert_agent.py)

- defines the policy agent role
- defines the `search_policies` tool schema

[app/agents/responder_agent.py](/Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/sentinel-ai-hub/app/agents/responder_agent.py)

- defines the responder role
- defines tool schemas for shipment/slack/maps style actions

Right now these files are mainly configuration and tool definitions.
The live orchestration is still happening in your Python app, not fully delegated to a server-side Foundry multi-agent runtime.

### Search / Retrieval

[app/core/search_client.py](/Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/sentinel-ai-hub/app/core/search_client.py)

- creates embeddings
- queries Azure AI Search
- runs hybrid retrieval

### Document Parsing

[app/core/document_intel.py](/Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/sentinel-ai-hub/app/core/document_intel.py)

- calls Azure AI Document Intelligence
- extracts structured document content for ingestion

### Tool Bridge

[app/tools/mcp_bridge.py](/Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/sentinel-ai-hub/app/tools/mcp_bridge.py)

- manages MCP stdio servers
- discovers available tools
- executes tool calls

[app/tools/mcp_server.py](/Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/sentinel-ai-hub/app/tools/mcp_server.py)

- local mock MCP tool server

### Guardrails

[app/core/safety_evaluator.py](/Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/sentinel-ai-hub/app/core/safety_evaluator.py)

- optional safety / groundedness validation
- currently falls back locally when Azure evaluation config is missing

## 4. Why The Confusion Happened

Your confusion is reasonable because Microsoft changed both branding and API shape.

There are two separate changes mixed together:

### Branding change

- Azure AI Foundry has been renamed to Microsoft Foundry.
- older docs, SDK examples, and portal screens still use Azure AI Foundry / AI Studio wording

### API and architecture change

Older agent patterns used concepts like:

- assistants
- threads
- messages
- runs
- preview `api-version` strings

The newer direction uses:

- conversations
- items
- responses
- agent versions
- more stable `/openai/v1/` style routes

So you were dealing with both:

- old names vs new names
- old runtime model vs new runtime model

That is why the code felt inconsistent.

## 5. V1 vs V2 Mental Model

This is the most important section.

### Version 1 style

Think:

- "assistant object"
- create thread
- add message
- create run
- poll run
- handle `requires_action`
- submit tool outputs

This is the older Assistants pattern.

It feels like:

1. create container for conversation
2. append messages
3. launch execution
4. wait for lifecycle states

### Version 2 style

Think:

- response
- conversation
- tool calls embedded in the response
- send tool results back with `previous_response_id`

This is closer to a single iterative response loop.

It feels like:

1. send input
2. get response
3. if tool calls exist, execute them
4. send tool outputs back
5. continue until final text arrives

### Practical difference

V1 is more object-heavy.
V2 is more response-loop oriented.

That means your current code should mentally be read as:

- "ask model"
- "inspect tool calls"
- "execute tools"
- "continue response"

not as:

- "create thread"
- "create run"
- "poll run states"

## 6. What "Agents" Mean In This Repo

You currently have two different meanings of "agent" in the same project.

### Meaning A: conceptual agent

Examples:

- `PolicyExpertAgent`
- `ResponderAgent`

These are role definitions:

- instructions
- model selection
- tool schema

### Meaning B: runtime orchestration code

Example:

- `SentinelOrchestratorAgent`

This is normal Python application logic that controls the flow.

So today your system is best described as:

"An application-managed multi-role agent workflow"

not yet:

"A fully server-managed Foundry multi-agent runtime"

That distinction is important.

## 7. What "Multi-Agent" Means Here

Right now, multi-agent mostly means:

- you defined multiple specialist personas
- you grouped tools by role
- the orchestrator coordinates the process

It does not yet mean that Foundry Agent Service itself is hosting multiple independently conversing agents end to end.

In other words:

- your app is doing the orchestration
- the model is doing tool selection
- Foundry stores agent definitions and versions

This is still a valid architecture.
It is just not the most "fully managed Agent Service" architecture possible.

## 8. How MCP Fits In

MCP is the tool bus.

Without MCP, the model can only generate text.
With MCP, the model can ask for actions or external facts.

In your flow:

1. the model returns a function/tool call
2. Python inspects the requested tool
3. `mcp_bridge.py` routes the call to the right MCP server
4. the MCP server executes the tool
5. Python sends the output back to the model

That means MCP is below the LLM in the stack:

- LLM decides
- Python orchestrates
- MCP executes

## 9. The Most Useful Way To Organize This Code

Use these layers.

### Layer 1: ingestion

- document parsing
- chunking
- embedding
- indexing

Suggested home:

- `app/ingestion/`

### Layer 2: runtime

- event consumers
- orchestrators
- conversation loops
- response handlers

Suggested home:

- `app/runtime/`

### Layer 3: capabilities

- retrieval
- safety
- model clients
- foundry project clients

Suggested home:

- `app/services/`

### Layer 4: tools

- MCP bridge
- local MCP server
- tool adapters

Suggested home:

- `app/tools/`

### Layer 5: agent definitions

- instructions
- tool schemas
- model bindings

Suggested home:

- `app/agents/definitions/`

### Layer 6: infrastructure config

- env parsing
- constants
- deployment-specific wiring

Suggested home:

- `app/config/`

## 10. Recommended Simplified Architecture

If you want less confusion, use this rule:

- Foundry project client for project metadata, registry, and governance
- Azure OpenAI endpoint for runtime inference
- Document Intelligence only during ingestion
- Azure AI Search only during retrieval
- MCP only for external tools

That is effectively how this repo is behaving after the fixes.

## 11. Current Repo Reality

As of this document, the repo works like this:

- Foundry project endpoint is used for `AIProjectClient` and agent version registration.
- Direct Azure OpenAI endpoint is used for `responses.create(...)`.
- Azure AI Search is required for policy retrieval.
- Document Intelligence is part of the document ingestion pipeline.
- MCP provides mock and optional external operational tools.

This is a pragmatic hybrid architecture.

It is not wrong.
It is just more hybrid than the original "all-in Foundry" mental model.

## 12. The Clean One-Sentence Definitions

Use these in interviews or design docs.

- Microsoft Foundry: the Azure platform for building, governing, and operating AI apps and agents.
- Azure OpenAI: the managed model inference service for GPT and embeddings on Azure.
- Azure AI Document Intelligence: the document extraction service for OCR, layout, and structured parsing.
- Azure AI Search: the retrieval engine for keyword, vector, and semantic search.
- MCP: the protocol that lets models invoke tools and external systems.

## 13. The Biggest Mistakes To Avoid

- Do not treat Foundry as if it is the same thing as Azure OpenAI.
- Do not treat Document Intelligence as if it is a chat model.
- Do not treat Search as if it is the LLM.
- Do not mix old Assistants/Threads mental models with new Responses mental models in the same flow unless you have a specific reason.
- Do not assume "multi-agent" automatically means the platform is doing the orchestration for you.

## 14. What I Would Do Next In This Repo

1. Split "agent definitions" from "runtime orchestration".
2. Add a small architecture README showing ingestion vs runtime.
3. Standardize on one runtime inference path.
4. Remove any remaining threads/runs terminology from comments and docs.
5. Provision and ingest Azure AI Search data so retrieval actually works.

## 15. Sources

These were the main references used for the mental model and current terminology:

- Microsoft Foundry overview: https://learn.microsoft.com/en-us/azure/ai-foundry/
- What is Microsoft Foundry: https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry
- Foundry evolution and terminology shift: https://learn.microsoft.com/en-us/%20azure/ai-foundry/azure-openai-in-azure-ai-foundry
- Foundry Agent Service overview: https://learn.microsoft.com/azure/ai-foundry/agents/overview
- Document Intelligence overview: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/
- Azure OpenAI / Foundry Models overview: https://learn.microsoft.com/azure/ai-services/openai/overview
