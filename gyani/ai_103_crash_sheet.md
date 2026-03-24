# AI-103 Crash Sheet

This sheet is for the replacement certification path:

- `AI-103`: Azure AI App and Agent Developer Associate

Important date note:
- Microsoft’s Skills Hub update published on **March 3, 2026** lists `AI-102` as retiring on **July 31, 2026**, with `AI-103` as the replacement.

Official references:
- Skills Hub retirement/update post: <https://techcommunity.microsoft.com/blog/skills-hub-blog/the-ai-job-boom-is-here-are-you-ready-to-showcase-your-skills/4494128>
- AI-103 course page: <https://learn.microsoft.com/en-us/training/courses/ai-103t00>
- Microsoft Foundry learning path: <https://learn.microsoft.com/training/paths/get-started-ai-apps-agents/>

## What Is Different From AI-102

`AI-103` appears to shift the focus from broad Azure AI services coverage toward:

- AI apps on Azure
- agent development
- Microsoft Foundry
- generative AI workflows
- multi-step reasoning
- production-ready agents
- knowledge connections and tool integration
- multimodal capabilities

This means the exam is likely more aligned to modern agentic application development than older service-by-service Azure AI coverage.

## What To Study First

### Highest priority

- Microsoft Foundry basics
- generative AI app architecture
- AI agents
- tool calling
- knowledge connections
- RAG
- multi-step workflows
- prompt patterns
- production reliability for AI apps
- security and governance basics

### Medium priority

- multimodal capabilities
- document/content understanding
- observability and evaluation
- deployment patterns

### Lower priority for a crash plan

- legacy Azure AI service trivia
- low-level SDK syntax memorization
- older exam-style service taxonomy details

## Core Mental Model

Think in this sequence:

1. User asks for help
2. App decides whether simple generation is enough
3. If not, agent retrieves knowledge or calls tools
4. Agent reasons through multiple steps
5. App validates or filters outputs
6. System logs quality, latency, and token usage
7. Production controls handle security, errors, and scale

If you understand that model well, you will likely be prepared for the center of the exam.

## Service / Platform Map

### Microsoft Foundry

Know this as the platform layer for building, managing, and deploying AI apps and agents.

You should be ready to explain:
- project setup
- model access
- orchestration concepts
- knowledge/tool integration
- evaluation and monitoring concepts

### Azure OpenAI

Use for:
- chat apps
- prompt-based generation
- embeddings
- reasoning workflows
- agent backends

Know:
- prompts
- system instructions
- temperature
- token limits
- structured outputs
- tool-calling concepts

### Knowledge Connections / RAG

Use when:
- enterprise data is private
- content changes often
- responses must be grounded
- citations or factual backing matter

Know:
- chunking
- embeddings
- retrieval
- grounding
- hallucination reduction
- search plus generation pattern

### Tools In Agentic Apps

Use when the assistant must do more than answer text.

Examples:
- look up enterprise data
- call APIs
- search documents
- run multi-step actions

Know:
- tool selection
- step orchestration
- when to use an agent versus simple prompt flow
- risks of uncontrolled tool access

### Multimodal / Complex Content

Based on the course description, expect coverage around:
- text plus document understanding
- image or rich-content interpretation
- handling complex inputs in AI apps

You do not need deep research-level knowledge. You need service-selection and architecture-level judgment.

## Likely Exam Themes

These are inferred from Microsoft’s current training/course descriptions.

### 1. Build generative AI apps

Be ready for:
- chat app architecture
- prompt design
- model selection concepts
- app flow design
- API/SDK usage patterns

### 2. Build AI agents

Be ready for:
- agent role definition
- tools
- planning and reasoning workflows
- multi-step execution
- multi-agent coordination basics

### 3. Add knowledge and tools

Be ready for:
- RAG patterns
- enterprise search integration
- grounding
- knowledge connectors
- function and tool invocation

### 4. Productionize AI apps

Be ready for:
- monitoring
- evaluation
- responsible AI
- security
- deployment and reliability

### 5. Work with complex content

Be ready for:
- document-based inputs
- multimodal scenarios
- information extraction concepts

## What To Memorize

### Agent vs non-agent

Use a normal generative app when:
- one response is enough
- there is no need for tool calling
- the workflow is simple

Use an agent when:
- multiple steps are needed
- tools or enterprise systems must be called
- the app must reason through a workflow
- the solution needs adaptive routing

### RAG vs fine-tuning

RAG:
- private/current data
- faster updates
- better auditability
- better for enterprise knowledge

Fine-tuning:
- model behavior shaping
- repeated domain style or task patterns
- not the first answer for changing enterprise knowledge

### Tool calling

Good for:
- API lookups
- actions
- dynamic retrieval
- workflow execution

Risks:
- security
- unintended actions
- brittle orchestration
- poor observability if not instrumented

### Production-ready AI apps

Must include:
- authentication
- secret management
- logging and tracing
- latency awareness
- failure handling
- output validation
- cost awareness

## Two-Day Crash Plan

## Day 1

### Block 1: 2 hours

Study:
- Microsoft Foundry basics
- generative AI app flow
- Azure OpenAI concepts

Memorize:
- model + prompt + retrieval + tool + output validation

### Block 2: 2 hours

Study:
- agent concepts
- multi-step reasoning
- tool calling
- when to use agents

Memorize:
- agent = reasoning plus tools plus workflow
- not every chatbot should be an agent

### Block 3: 90 minutes

Study:
- RAG
- knowledge connections
- grounding patterns

Memorize:
- retrieve first, generate second
- private and changing data means RAG is usually preferred

### Block 4: 60 minutes

Review:
- multimodal and complex content
- document understanding concepts

## Day 2

### Block 1: 90 minutes

Study:
- responsible AI
- security
- governance
- safe deployment patterns

Memorize:
- least privilege
- secure secret handling
- content filtering
- auditability
- human oversight

### Block 2: 90 minutes

Study:
- observability
- evaluation
- latency and token/cost awareness
- production reliability

Memorize:
- if you cannot measure quality, latency, and failures, the app is not production-ready

### Block 3: 2 hours

Review all likely scenario patterns:
- simple chat app
- RAG app
- tool-using agent
- multi-agent workflow
- multimodal document workflow

### Block 4: 60 minutes

Final recall drill:
- when to use agent vs simple app
- when to use RAG
- what Foundry provides
- what makes AI apps production-ready

## Scenario Cheat Sheet

### If the question says

`Need grounded answers from enterprise documents`

Think:
- RAG
- knowledge connections
- retrieval plus generation

`Need the app to call APIs or enterprise tools`

Think:
- agent
- tool calling
- orchestration

`Need a workflow that decides across multiple steps`

Think:
- agentic pattern
- possibly multi-agent or orchestrated workflow

`Need production-ready deployment`

Think:
- monitoring
- evaluation
- security
- cost/latency
- controlled rollout

`Need to handle documents or complex content`

Think:
- multimodal or document understanding flow
- extract, ground, reason, validate

## Interview / Exam Answer Pattern

For almost every scenario, answer internally using this order:

1. What is the user goal?
2. Does this require generation only, or an agent?
3. Does it need enterprise knowledge grounding?
4. What tools or connections are needed?
5. How is it secured?
6. How is it monitored and evaluated?

## Best Way To Use Your Existing Background

You already understand:
- RAG
- LangGraph-style agent orchestration
- observability
- guardrails
- resilient routing

For `AI-103`, the fast path is to remap that knowledge into Microsoft’s newer framing:
- Foundry
- AI apps
- agents
- knowledge connections
- production-ready orchestration

## What To Ignore In A Crash Prep

- deep memorization of old service menus
- obscure legacy Azure AI service details
- implementation trivia that does not change the architecture decision

## Final Advice

- If the public `AI-103` exam page becomes available before you schedule, review the official skills outline once and adjust this sheet.
- Until then, this sheet is the best fast-prep path based on Microsoft’s current replacement announcement and `AI-103T00-A` training description.
