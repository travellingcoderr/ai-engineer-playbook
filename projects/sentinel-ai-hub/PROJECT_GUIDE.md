# Project Sentinel: Enterprise AI Foundry Guide

This guide provides everything you need to set up, understand, and demonstrate **Project Sentinel** as an Azure AI Foundry Specialist.

---

## 1. The Strategy: Problem & Solution Architecture

Sentinel is a production-grade solution to the challenge of **Automated Enterprise Risk Mitigation**. It bridges the gap between "hearing about a problem" and "taking action on it."

### 1.1 The "Wall of Text" Problem (Document Intelligence)
*   **The Problem**: Contracts (SLAs) are messy PDFs with complex tables. Standard AI reads them as a "wall of text," losing structural meaning (e.g., merging separate clauses).
*   **Sentinel Solution**: We use **Azure AI Document Intelligence** (`prebuilt-layout`) to extract **High-Fidelity Markdown**. This preserves headers and tables, allowing the AI to "see" the legal structure and provide 100% reliable answers.

### 1.2 The "Stale Data" Problem (Hybrid RAG)
*   **The Problem**: A basic AI model only knows what it was trained on. Simple keyword search often misses context, and simple vector search can be imprecise.
*   **Sentinel Solution**: We implement **Hybrid Search** (Vector + Semantic). 
    *   **Vector** finds the general "concept" of the disaster.
    *   **Semantic** re-ranks the results using an L2 reranker to find the *exact* legal clause that matches the specific disruption.

### 1.3 The "Siloed AI" Problem (MCP Bridge)
*   **The Problem**: Most AI models are "trapped" in a chat window. They can't check Google Maps for traffic, check inventory, or send a Slack message.
*   **Sentinel Solution**: We use the **Model Context Protocol (MCP)**. This is a path-breaking "universal translator" that hooks your Azure AI Agents into external tools (Slack, Google Maps, Mock Logistics) in real-time.

### 1.4 The "Manual Orchestration" Problem (Multi-Agent Threads)
*   **The Problem**: A single AI agent trying to handle legal, logistics, and communication often gets confused and hallucinates.
*   **Sentinel Solution**: We use **Azure AI Foundry Threads** to orchestrate a team:
    *   **SentinelOrchestratorAgent**: Manages the Event Hub trigger and timeline.
    *   **PolicyExpertAgent**: Specializes only in reading/interpreting legal documents.
    *   **ResponderAgent**: Specializes in using tools (Maps/Slack) to execute the response.

---

## 2. Setting Up Azure Resources (CLI)

Run these commands to provision your environment from scratch.

### A. Resource Group & AI Foundry Hub
```bash
# Create Group
az group create --name sentinel-rg-007 --location eastus

# Create AI Foundry Hub
az ml workspace create --name sentinel-hub-007 --resource-group sentinel-rg-007 --location eastus
```

### B. Azure AI Search (Vector & Semantic Search)
```bash
az search service create \
    --name sentinel-search-007 \
    --resource-group sentinel-rg-007 \
    --sku Basic \
    --partition-count 1 \
    --replica-count 1
```

### C. Azure Document Intelligence
```bash
az cognitiveservices account create \
    --name sentinel-doc-intel-007 \
    --resource-group sentinel-rg-007 \
    --kind FormRecognizer \
    --sku S0 \
    --location eastus
```

### D. Azure Event Hubs
```bash
# Namespace
az eventhubs namespace create --name sentinel-eh-ns-007 --resource-group sentinel-rg-007 --location eastus

# Event Hub
az eventhubs eventhub create --name sentinel-events-007 --resource-group sentinel-rg-007 --namespace-name sentinel-eh-ns-007
```

---

## 3. Mock Data Strategy

### Internal Policies (Contracts)
We provide a sample **SLA_Warehouse_Miami.md**. In production, your `ingest_doc.py` script uses **Azure AI Document Intelligence** to convert raw PDFs into this structured Markdown format. Markdown is essential for RAG because it preserves the **semantic boundaries** of your clauses.

### Simulated Alerts
The `scripts/simulate_event.py` script sends a JSON disruption event:
```json
{
    "event_type": "Hurricane Alert",
    "city": "Miami",
    "severity": 9,
    "details": "Major Category 4 Hurricane Approaching..."
}
```

---

## 4. Vector Database Rationale: Hybrid Search
Your interview question "What is semantic search?" is answered here. Sentinel uses **Azure AI Search** for **Hybrid Retrieval**:
1.  **Vector Search**: Finds documents with similar "embeddings" (meaning). Useful for when words don't match exactly but concepts do.
2.  **Semantic Search**: A second-pass re-ranker that understands human language nuances (L2 ranking). 
**Why not just Pinecone?** Azure Search allows you to store your data *and* its vector in a single service, with industry-leading reranking logic that is specifically tuned for business documents.

---

## 5. Hooking in MCP (Model Context Protocol)

MCP is the open standard for connecting LLMs to external systems. Sentinel uses a `MultiMCPManager` bridge:

-   **Mock Server (`mcp_server.py`)**: A local Python subprocess providing logistics tools.
-   **Remote Servers (Slack/Maps)**: Node.js servers run via `npx`.
**How to Hook:**
1.  Your Agent sends a `requires_action` request to the project client.
2.  The Orchestrator captures it and routes it to the `mcp_manager`.
3.  The manager executes the tool on the corresponding MCP stdio server and returns the JSON result.

---

## 🛠️ Testing the Use Case

### Method A: Local Setup
1.  Update `.env` with your Azure keys.
2.  `make setup`
3.  `make provision` (Setup Search Index)
4.  `make ingest` (Index the Miami SLA)
5.  `make run` (Starts the hub in Simulation Mode)

### Method B: Docker (Recommended)
1.  `make docker-build`
2.  `make docker-run`

**Observe**: Watch the console logs! You'll see the Orchestrator delegating tasks: 
"Policy Expert searching for Hurricane Protocol..." -> "Responder checking shipment status and posting to Slack..."

---

## 6. Technical Deep Dive & Interview FAQ

### 6.1 What exactly is `prebuilt-layout`? (Document Intelligence)
*   **The Nuance**: It is a "Multi-modal" model. It doesn't just read text; it uses computer vision to understand the **geometric layout** of the page.
*   **How it works**: It identifies the physical boundaries of tables, headers, and paragraphs. Crucially, it reconstructs the **Reading Order**. 
*   **The Vector DB impact**: It doesn't just "take text near a table." It converts the table into **Markdown code** (`|---|`). When this Markdown is stored in your vector database, the LLM can "understand" the relationship between a row and a column. 
*   **Versatility**: Because it uses vision, it works on any document type (invoices, legal contracts, engineering diagrams) without needing a pre-defined template.

### 6.2 Why is simple vector search imprecise? (Vector vs. Semantic)
*   **The "Distance" Problem**: Vector search is based on **Cosine Similarity** (mathematical distance). It finds words that are "near" each other in meaning, but it doesn't understand **intent**. 
*   **The L2 Reranker (Semantic)**: Think of Vector Search as a "Wide Net" and the Reranker as a "Microscope." 
*   **The Workflow**: We make **one** vector call to get the top 50 results (fast and cheap). Then, we send those 50 results to the **Semantic Reranker** (L2). The reranker is a much larger model that does a deep linguistic analysis to see which of those 50 actually answers the query. It doesn't need 5 calls; it just needs a small "candidate list" to work its magic.
 
 ```python
 # --- Fast and Cheap Vector-Only Retrieval ---
 vector_query = VectorizedQuery(
     vector=query_vector, 
     k_nearest_neighbors=50,  # Fast Cosine Similarity for the top 50
     fields="content_vector"
 )
 
 # One call to fetch candidates before expensive re-ranking
 results = search_client.search(
     search_text=None, 
     vector_queries=[vector_query],
     top=50
 )
 ```
 
 > [!TIP]
 > **Why "Fast and Cheap"?** Pure vector search is a direct mathematical distance calculation on a pre-computed index (HNSW). Semantic Reranking, however, is a secondary pass where each candidate is processed by a much larger, more expensive model. Using Vector search as a "filter" is the industry standard for performance.

### 6.3 MCP Protocol—Reinventing the wheel? (MCP vs. Custom API)
*   **The Protocol**: MCP uses a standard called **JSON-RPC** over `stdio` (Standard Input/Output). 
*   **Leveraging vs. Creating**: We are **leveraging**. You are **not** writing the code to talk to Slack's API or Google's API. You are simply using the **Standardized Wrapper** provided by the companies. 
*   **The Benefit**: This allows an Azure Agent to talk to any tool in the world as long as that tool has an MCP wrapper. You focus on the **Orchestration**, not the low-level API integration.

### 6.4 What is an AI Thread vs. App Thread? (Agents & Concurrency)
*   **AI Thread**: This is a **Cloud-Stored Session**. Unlike your React app's thread (which dies when the page refreshes) or your Node.js event loop, the AI Thread is a persistent database record on Azure that stores the entire history, state, and "memory" of that specific conversation.
*   **The Thread ID Lifecycle**: Your React app doesn't know the ID "beforehand." 
    1. **Creation**: When a user first chats, your backend calls `create_thread()` on Azure.
    2. **Handoff**: The backend returns the `thread_id` to your React app in the HTTP response.
    3. **Persistence**: The React app saves it (e.g., in `localStorage`).
    4. **Resumption**: In all future messages, the React app sends that ID back to the backend. This is how Azure knows to "resume" the specific conversation instead of starting a new one.
*   **Agents in Sentinel**: There are **3 agents**:
    1.  **SentinelOrchestratorAgent**: The "Brain" that manages the logic.
    2.  **PolicyExpertAgent**: The "Researcher" that has the Search tool.
    3.  **ResponderAgent**: The "Worker" that has the Slack/Maps tools.
---
 
 ## 7. The Interview Bible: Patterns & Responsible AI
 
 ### 7.1 The 8 AI & Prompt Design Patterns
 If an interviewer asks for "AI Patterns," they are usually referring to these 8 concepts. Sentinel implements the most advanced ones (4-8) natively:
 
 1.  **Persona/Role-Based**: Assigning specific identities (e.g., "You are a Logistics Specialist").
 2.  **Chain-of-Thought (CoT)**: Forcing the model to "think step-by-step."
 3.  **Few-Shot**: Providing examples within the prompt to guide the output.
 4.  **Reflection (implemented)**: The ResponderAgent reviews its own tool outputs to ensure they meet the goal.
 5.  **Tool Use (implemented)**: Our **Multi-MCP Manager** allows the AI to "reach out" into the real world.
 6.  **Planning (implemented)**: The Orchestrator creates a multi-step execution plan based on the Event Hub alert.
 7.  **Multi-Agent Collaboration (implemented)**: Orchestrator, Policy Expert, and Responder work as a team.
 8.  **Routing (implemented)**: The Orchestrator "routes" the specific problem to the correct specialized agent.
 
 ### 7.2 Responsible AI (RAI) in the Project
 In Azure AI Foundry, "Responsible AI" is more than just a buzzword; it's a structural requirement.
 *   **Content Safety**: Automatically filters for hate, violence, and self-harm.
 *   **Groundedness**: This is the core of our **RAG** strategy. By only allowing the AI to answer based on the indexed SLA, we prevent "hallucinations," which is a primary goal of Responsible AI.
 *   **jailbreak Detection**: Protects your agent from "Ignore all previous instructions" attacks.
 
 ### 7.3 What about Diffusion Models?
 While Sentinel uses **Transformers** (LLMs for text), Diffusion Models (Stable Diffusion, Midjourney) are for **Image/Media Generation**.
 *   **How they work**: They start with a image made of random "noise" and slowly subtract that noise (Denoising) until a clear image emerges.
 *   **Key Concept**: The "Forward Process" adds noise; the "Reverse Process" removes noise based on your text prompt.
 
 ### 7.4 Tokenization & Embeddings: The Math of Azure AI
 *   **The Tokenizer (`cl100k_base`)**: Before an AI reads text, it breaks it into "tokens" (chunks of characters). We use the **cl100k_base** tokenizer, which is the same one used by GPT-4 and GPT-4o. It is highly efficient at handling a wide range of languages and technical jargon.
 *   **The Embedding Model (`text-embedding-3-small`)**: This is the "brain" that converts those tokens into a **1536-dimensional vector** (a list of 1,536 numbers). 
 *   **The Concept of "Vector Distance"**: In Azure AI Search, we find the best SLA match by calculating the mathematical distance between your query's vector and the document's vector. The closer they are in 1,536-dimensional space, the more "semantically similar" they are.
 *   **Why 1536?**: This specific dimensionality is the gold standard for balancing high-performance retrieval with storage efficiency.
