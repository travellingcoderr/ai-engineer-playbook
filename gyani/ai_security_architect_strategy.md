# AI Security Architect – Strategy & Role Mapping

This document provides a tailored strategy for securing a high-level **AI Security Architect** role, specifically focused on the Commvault opportunity and similar advanced positions.

---

## 1. The "Golden Thread" – Connecting Your Past to the Role
Your profile is unique because it blends **Enterprise Compliance (PwC)** with **State-of-the-Art AI Orchestration (EPM/Rocket)**.

- **PwC (Senior Manager, Compliance Software):** This provides the "Who You Are" foundation (5+ years in security/product roles, communicating with leadership, and structured writing for reviews).
- **EPM/Rocket (AI Architect):** This provides the "What You’ll Do" technical edge (LangChain, LangGraph, agentic workflows, and multi-agent systems).

---

## 2. Mapping Your Expertise to Commvault's Needs

| Commvault Requirement | Your Specific Proof Point |
| :--- | :--- |
| **"Identify and assess security risks associated with AI/ML systems"** | Leveraging your PwC background to conduct threat modeling for agentic workflows (e.g., assessing the risk of tool selection loops in LangGraph). |
| **"Mitigate risks such as prompt injection and data leakage"** | Highlighting your implementation of guardrails and policy enforcement for enterprise agents at EPM. |
| **"Secure AI-related data sources"** | Your deep expertise in Snowflake, Databricks, and Oracle provides the foundation for securing the "training datasets and model artifacts" they mention. |
| **"Agentic workflows and multi-agent architecture"** | This is your strongest differentiator. You are already an expert in the exact "Nice to Have" tools they listed (LangChain, LangGraph). |

---

## 3. Resume & LinkedIn High-Impact Bullets

To "wow" the recruiter for this role, use these specific phrasing patterns:

- **Instead of:** "Built AI agents using LangChain."
- **Use:** "Architected secure **agentic workflows** using **LangGraph**, implementing **constraint enforcement** and **policy guardrails** to prevent unauthorized tool execution and prompt injection."

- **Instead of:** "Managed compliance software at PwC."
- **Use:** "Led security architecture and threat modeling for an **enterprise compliance platform**, translating complex regulatory risks into technical controls for distributed data systems."

- **Instead of:** "Expert in SQL and Snowflake."
- **Use:** "Designed secure **data pipelines** for AI ingestion on **Snowflake/Databricks**, ensuring data privacy (PII) and integrity during RAG retrieval phases."

---

## 4. Interview "AI Security" Deep Dives
Prepare specific answers for these anticipated questions:

1.  **"How do you secure an agent that has 'tool use' capabilities?"**
    - *Answer Focus:* Discuss least-privilege for tools, human-in-the-loop for destructive actions, and state management filters to prevent tool-selection loops.
2.  **"What is the biggest risk when using RAG with sensitive documents?"**
    - *Answer Focus:* Data leakage during retrieval (e.g., a user retrieving a summary that includes PII from a document they shouldn't see). Discuss row-level security and vectorized ACLs.
3.  **"How does your compliance background help in AI innovation?"**
    - *Answer Focus:* It allows you to build "Security-by-Design." Instead of stopping innovation, you provide the "guardrails" that allow data scientists to move fast without risking the enterprise.

---

---

## 5. The Six Pillars of AI Security (OWASP Top 10 + Production Risks)
In your role as an AI Security Architect, you will need to articulate and defend against these 6 core vulnerability classes. We have already begun implementing these as modular "Guardrails" in your playbook.

### 1. Prompt Injection (Direct & Indirect)
*   **The Problem:** Overriding system instructions via user input. Indirect injection occurs when malicious data is ingested through RAG (PDFs, URLs).
*   **Our Solution:** `InjectionService` uses fuzzy regex patterns. Future-proofing includes **LLM-based oversight** to scan retrieved RAG context for hidden instructions.

### 2. Token Smuggling
*   **The Problem:** Encoding malicious payloads (Base64, ROT13, Unicode) to bypass simple regex filters.
*   **Our Solution:** `SmugglingService` decodes various encodings and re-scans the payload. We are expanding this to detect **Unicode homoglyphs**.

### 3. Denial-of-Wallet & Model DoS
*   **The Problem:** Attackers draining cloud budget via massive token requests or saturating inference capacity.
*   **Our Solution:** `DoSService` implements **token-count estimation** and strict input length enforcement before passing requests to the model.

### 4. Data Exfiltration
*   **The Problem:** Subtle prompts designed to leak system instructions, training data, or session PII.
*   **Our Solution:** Combined `InjectionService` and `SafetyService` look for "reveal system prompt" and extraction-style framing.

### 5. Malformed & Malicious Outputs
*   **The Problem:** Models returning invalid JSON or jailbroken harmful content that targets the end-user.
*   **Our Solution:** `OutputService` validates the structural integrity (schema) and safety of every model response.

### 6. Missing/Misconfigured Authentication
*   **The Problem:** Publicly exposed API endpoints (/chat) being harvested by scanners.
*   **Our Solution:** Implementing **API Key middleware** and rate-limiting keyed to identifiers, not just IP addresses.

---

## 6. Recommended Skill/Certification "Fillers"
*   **Prompt Injection Defense:** Follow the OWASP Top 10 for LLMs.
*   **Security Cert:** If you don't have it, consider the **CCSP (Certified Cloud Security Professional)** to double down on cloud architecture security.
*   **AI Policy:** Familiarize yourself with the **NIST AI Risk Management Framework**.

---

## Next Steps
1.  **Update your LinkedIn headline:** `AI Security Architect | Enterprise AI Orchestration | LangGraph | Compliance & Risk Management`.
2.  **Reach out to the hiring manager:** Mention your bridge between PwC compliance and Rocket Mortgage AI labs.
