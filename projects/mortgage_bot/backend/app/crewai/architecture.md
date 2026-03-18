# Mortgage Bot CrewAI Architecture

## Purpose

This CrewAI integration exists to teach how a multi-agent team differs from the existing LangGraph ReAct implementation in the same mortgage bot.

The goal is not to replace LangGraph. The goal is to compare:

- LangGraph for explicit ReAct workflows and tool loops
- CrewAI for role-based multi-agent collaboration

## Why CrewAI fits this project

Mortgage support questions often benefit from more than one perspective:

- intake and issue framing
- loan operations analysis
- guideline or policy research
- final resolution writing

CrewAI is useful when you want those roles to be modeled explicitly as a team.

## Current CrewAI learning use case

This repo uses a single CrewAI use case:

- `mortgage issue triage crew`

It is designed for questions like:

- `Why is LN-1002 stuck and what should I do next?`

## Agent roles

The current crew has four agents:

- `Mortgage Intake Analyst`
  - identifies the issue and frames the problem
- `Mortgage Loan Ops Specialist`
  - analyzes milestone, loan details, and conditions
- `Mortgage Guidelines Researcher`
  - reviews supporting knowledge and guidance
- `Mortgage Resolution Writer`
  - combines the work into a final triage summary

## How this integrates with the mortgage bot

The CrewAI path reuses the existing mortgage MCP-style tools before the crew runs:

- `get_loan_details`
- `list_loan_conditions`
- `get_milestone_history`
- `search_knowledge`

Those tools gather structured context first. That context is then passed into CrewAI tasks so each agent has relevant mortgage data to work from.

This design keeps the learning path simple:

- MCP-style tools gather data
- CrewAI agents collaborate on interpretation
- the final output is a role-based triage summary

## Files

- `agents.py`
  - defines CrewAI agent roles
- `tasks.py`
  - defines the work given to each role
- `crew.py`
  - gathers mortgage context, builds the crew, and runs the workflow

## Why not let every CrewAI agent call tools directly

For a first learning pass, the project gathers the mortgage context first and then feeds that into the crew.

That makes it easier to understand:

- what came from tools
- what came from the crew
- how the output was synthesized

Later, you can evolve this into direct agent-tool integration if you want a more autonomous CrewAI setup.

## Comparison with LangGraph

LangGraph path:

- one agent
- ReAct loop
- agent decides when to call tools
- best for explicit workflow control

CrewAI path:

- multiple role-based agents
- sequential collaboration
- best for learning specialization and task handoff

## Learning objective

By keeping both orchestration styles in the same mortgage bot, you can compare them on the same user question and understand:

- when a single-agent ReAct loop is enough
- when a multi-agent team adds value
- how mortgage MCP-style tools can be reused in both approaches
