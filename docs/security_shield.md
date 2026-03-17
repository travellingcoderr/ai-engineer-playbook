# OWASP Top 10 for LLMs - Security Shield

This document maps the **AI Engineer Playbook** Guardrails and Gateway patterns to the OWASP Top 10 LLM risks, providing a blueprint for secure enterprise AI deployment.

## 🛡 Risk Mapping & Mitigation

| OWASP Risk | Description | Playbook Mitigation |
| :--- | :--- | :--- |
| **LLM01: Prompt Injection** | Manipulating LLM via crafted inputs. | `projects/guardrails` uses semantic filtering and PII detectors to flag injection patterns. |
| **LLM02: Insecure Output Handling** | Trusting LLM output without validation. | `AuditLogMiddleware` and output guardrails in the Gateway validate syntax before returning. |
| **LLM03: Training Data Poisoning** | Compromising the model's knowledge. | **Phase 4**: Golden Dataset Evals in `ai_perf_eval` catch drifts or "hallucinated" regressions. |
| **LLM04: Model Denial of Service** | Overloading LLM leading to high costs/latency.| `resilient_gateway` uses rate-limiting and circuit breakers to prevent service exhaustion. |
| **LLM06: Sensitive Data Disclosure**| LLM revealing PII/Confidential data. | `projects/guardrails` PII Redaction filters both inputs and outputs. |
| **LLM07: Insecure Plugin Design** | Plugins/Tools with excessive permissions. | **NHI Pattern**: Scoped access tokens for MCP tools ensures agents only touch what they need. |
| **LLM10: Model Theft** | Unauthorized access to model weights/APIs. | `mcp_gateway` provides a centralized authenticated hub, hiding raw API keys from clients. |

## 🚀 Security Implementation Strategy

1. **Input Shielding**: Always wrap your calls through the `resilient_gateway` to ensure guardrails are applied globally.
2. **Output Sanitization**: Use the Gateways `LLMResponse` model to enforce structured output, reducing the risk of XSS or command injection in the UI.
3. **Continuous Evals**: Run `make eval` regularly to ensure your security prompts are still effectively blocking injections as models evolve.
