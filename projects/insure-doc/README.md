# InsureDoc: AI-Powered Dental Claims Platform

**InsureDoc** is a professional demonstration of a containerized, local-first AI platform for insurance claim analysis. It uses **LangGraph**, **ChromaDB**, and **Azure OpenAI** to automate the review of "stuck" dental claims against complex policy manuals.

---

## 🏗️ Architecture
The platform is built as a set of coordinated microservices:
- **[Ingestion Service](./docs/GETTING_STARTED.md)**: Document chunking and vectorization (Port 3001).
- **[Claim Service](./docs/GETTING_STARTED.md)**: Real-time claim status and snapshot engine (Port 3002).
- **[Orchestrator Service](./docs/GETTING_STARTED.md)**: Multi-agent reasoning brain (Port 3003).

---

## 🚀 Quick Start
1. **Initialize Your Environment**:
   ```bash
   bash scripts/local-setup.sh
   # Edit the .env file with your Azure OpenAI keys
   ```
2. **Launch the Platform**:
   ```bash
   docker-compose up -d --build
   ```
3. **Analyze Your First Claim**:
   Visit [`http://localhost:3003/api-docs/`](http://localhost:3003/api-docs/) to use the Interactive AI Chat!

---

## 📚 Documentation
- **[Getting Started](./docs/GETTING_STARTED.md)**: Detailed onboarding and architecture overview.
- **[Azure AI Setup](./docs/AZURE_SETUP.md)**: Step-by-step guide to provisioning your AI infrastructure.

---

## 📄 Mock Knowledge Base
The platform includes 10 procedure-specific mock insurance booklets (D2740-D6010) located in the **`docs/`** folder, generated via `scripts/generate-docs.js`.
