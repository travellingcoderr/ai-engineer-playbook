# Getting Started - InsureDoc

**InsureDoc** is a multi-agent system for dental claim analysis. It uses three containerized microservices to coordinate between claim data and policy manuals.

---

## 🏗️ 1. Architecture Overview
- **Ingestion Service (3001)**: Processes and vectorizes PDF/text policy manuals (ChromaDB).
- **Claim Service (3002)**: Manages real-time claim status and snapshots (MongoDB).
- **Orchestrator (3003)**: The AI Agent that reasons between claims and policies (LangChain/LangGraph).

---

## 🛠️ 2. Rapid Local Setup
1. **Configure Your Environment**:
   - Run `bash scripts/local-setup.sh` at the project root.
   - Edit the newly created `.env` file at the root with your **Azure OpenAI** credentials.
2. **Start the Stack**:
   - Run `docker-compose up -d`.
3. **Verify Health**:
   - Visit [`http://localhost:3003/api-docs/`](http://localhost:3003/api-docs/) to see the AI agent's documentation.

---

## 📊 3. Common Commands
- **View All Logs**: `docker-compose logs -f`
- **Rebuild One Service**: `docker-compose up -d --build orchestrator-service`
- **Clean Slate**: `docker-compose down -v` (removes all volumes and data).
