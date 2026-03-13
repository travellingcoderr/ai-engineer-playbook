# OWASP LLM Risks and Guardrails Cheat Sheet

This file is here because security knowledge is a differentiator.

## Why this matters

Companies do not just want people who can call a model API. They want people who understand how AI systems fail in the real world.

OWASP maintains a Top 10 for LLM applications and broader GenAI security guidance. The published risks include prompt injection and insecure output handling among the key issues. citeturn584966search3turn584966search11turn584966search23

## The risks you should be ready to discuss

### Prompt injection
A malicious or crafted input tries to override instructions or manipulate tool use.

### Insecure output handling
The model returns content that gets executed or trusted without validation.

### Data leakage
Sensitive internal information is exposed through prompts, retrieval, logs, or tool outputs.

### Excessive agency
An agent is allowed to take actions it should never have been able to take automatically.

### Over-reliance
Humans trust the answer too quickly even when the system is uncertain or wrong.

## Guardrails to implement

### Input guardrails
- classify risky requests
- filter malicious patterns
- isolate system prompts
- limit tool availability by context

### Tool guardrails
- read-only by default
- schema validation
- allowlists
- argument constraints
- human approval for high-risk actions

### Output guardrails
- sanitize output before downstream execution
- enforce structured formats
- redact secrets and PII where needed
- block unsafe action suggestions in sensitive domains

### Operational guardrails
- audit logs
- anomaly monitoring
- rate limiting
- abuse detection
- rollback / kill switch for risky tools

## Interview-ready line

> I treat guardrails as a system design problem, not just a model prompt problem. I apply them at input, tool, output, and operational layers.
