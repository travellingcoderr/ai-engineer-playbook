# Azure AI Document Intelligence: Setup & Integration Guide

This guide provides the professional steps to provision and integrate the **Azure AI Document Intelligence** service for the InsureDoc platform. This service enables high-fidelity **Markdown** extraction from PDFs, preserving complex tables for RAG analysis.

---

## ☁️ 1. Provisioning the Service (Azure Portal)

1.  **Sign In**: Access the [Azure Portal](https://portal.azure.com).
2.  **Search**: Use the top search bar to find **"Document Intelligence"** (formerly Form Recognizer).
3.  **Create**: Click the **+ Create** button to start a new instance.
4.  **Basics Tab**:
    - **Subscription**: Select your active Azure subscription.
    - **Resource Group**: Use the same group as your OpenAI and app services.
    - **Region**: Recommended: **East US**, **West US 2**, or **North Europe** (for latest feature support).
    - **Name**: e.g., `di-insuredoc-dev-001`.
    - **Pricing Tier**: Select **Free F0** (limited to 500 pages/mo) or **Standard S0**.
5.  **Identity Tab**: Enable **System-assigned managed identity** (Best Practice for secure authentication).
6.  **Review + Create**: Complete the deployment.

---

## 🔐 2. Retrieving Credentials

1.  Navigate to your new **Document Intelligence** resource.
2.  On the left sidebar (under Resource Management), click **Keys and Endpoint**.
3.  Copy the following values:
    - **Key 1**: Your primary authentication secret.
    - **Endpoint**: e.g., `https://di-insuredoc-dev-001.cognitiveservices.azure.com/`.

---

## 📂 3. Environment Configuration

Paste the credentials into your project's **[.env](file:///Users/works/Desktop/@sathish/ai_projects/ai-engineer-playbook/projects/insure-doc/.env)** file:

```bash
# --- AZURE DOCUMENT INTELLIGENCE (PHASE 5) ---
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=PASTE_YOUR_ENDPOINT_HERE
AZURE_DOCUMENT_INTELLIGENCE_KEY=PASTE_YOUR_KEY_1_HERE
```

---

## ✅ 4. Verifying the 'Smart Ingest' Integration

Once configured, verify the link between Azure and your local dashboard:

1.  **Launch Dashboard**: Ensure your `ingestion-service` is running.
2.  **Toggle ON**: In the UI header, enable the **"SMART INGEST"** toggle (Emerald Glow).
3.  **Upload Table**: Select a PDF containing a dental co-pay table (e.g., `policy_table_sample.pdf`).
4.  **Inspect Logs**: Check the backend console for `🧠 Smart Ingest: Advanced Analyze with Azure AI...`.
5.  **Query Test**: Ask the AI: *"What is the co-pay for procedure D2740?"* 
    - **Pass Content**: The AI correctly identifies the value from the preserved Markdown table.

---

> [!TIP]
> **Performance Tip**: Large PDFs (50+ pages) may take 10-15 seconds to process in Smart Mode. This is because Azure is performing a full layout-aware structural analysis. For simple text-only docs, turn Smart Mode **OFF** to use the local `pdf-parse` engine for instant results.
