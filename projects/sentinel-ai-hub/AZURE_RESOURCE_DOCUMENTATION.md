# Azure Resource Documentation: Project Sentinel

This document identifies and explains the purpose of each Azure resource in the **`sentinel-rg-007`** resource group.

---

## 🏗️ Resource Breakdown

Based on the [Infrastructure Snapshot](images/azure_resources_screenshot.png), here is the inventory of our AI platform:

| Resource Name | Type | Purpose |
| :--- | :--- | :--- |
| **`sentinel-hub-007`** | AI Foundry Hub | The central management point for your AI project. It handles agent orchestration, project settings, and resource connections. |
| **`sentinel-search-007`** | Azure AI Search | Your **Vector Store**. It indexes your SLAs and provides "Hybrid Search" capabilities (Vector or Keyword). |
| **`sentinel-doc-intel-007`** | Document Intelligence | Turns your raw PDFs (e.g., SLAs) into high-fidelity Markdown for ingestion into the AI system. |
| **`sentinel-eh-ns-007`** | Event Hubs Namespace | The "Ear" of the system. It listens for incoming disruption events from external sources. |
| **`sentinelstorage19ff122f2`** | Storage Account | **(Auto-created)** Essential for the AI Foundry Hub. It stores large files like model weights, session data, and fine-tuning results. |
| **`sentinelkeyvault9c47cbbc`** | Key Vault | **(Auto-created)** The secure vault for API keys. Instead of using raw keys, the system retrieves them securely at runtime. |
| **`sentinelinsightsd7d2c703`** | Application Insights | **(Auto-created)** Provides the **Observability** engine. It traces every agent step, tool call, and token count. |
| **`sentineilogalytiaa30a86e`** | Log Analytics | **(Auto-created)** The underlying database that stores the monitoring and telemetry data for App Insights. |
| **`Application Insights Smart Detection`** | Action Group | **(Auto-created)** A system component used to send alerts (emails/SMS) when the system detects anomalies. |

---

## ❓ Why are there so many "Auto-Created" resources?

Azure AI Foundry follows a **managed infrastructure** model. It creates these resources automatically to ensure the system is **Enterprise-Ready** on day one:

1.  **Security (Key Vault)**: To comply with enterprise standards, AI keys should never be stored in plaintext. The hub automatically creates a Vault to manage them.
2.  **Persistence (Storage)**: The Hub is stateless. It needs a dedicated "disk" to store persistent agent data and workspace artifacts.
3.  **Observability (App Insights)**: To provide metrics on "Groundedness" and "Hallucinations," the Hub needs an analytics engine to collect and process telemetry.

## 🕵️ Where is the "OpenAI Search" service?

There is no single service with this name. In the Azure ecosystem, these are **Decoupled**:

*   **The Vector Database**: This is specifically **`sentinel-search-007`**. It is NOT named "OpenAI Search" because it can work with any LLM (Llama, Mistral, etc.).
*   **The LLM Provider**: You will need a **Cognitive Services: Azure OpenAI** resource. This appears as its own item in the resource group. 
*   **The Connection**: Inside the AI Foundry Portal, you "connect" these two separate services together. This separation is what gives you "Multi-Model" flexibility.

> [!TIP]
> **Interview Prep**: If asked about the infrastructure stack, you can say: *"We deployed a standard Azure AI Foundry Hub-and-Spoke model. It uses Azure AI Search for high-dimensional vector retrieval and automatically provisions Managed Identities (Key Vault/Storage) for enterprise security."*
