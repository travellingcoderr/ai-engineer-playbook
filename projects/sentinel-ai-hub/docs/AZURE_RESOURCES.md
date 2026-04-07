# Azure AI Foundry: Resource Utility Guide

This document explains how the various Azure resources linked to our Foundry project power the Sentinel AI Hub.

## 🧠 Core Intelligence: Azure OpenAI
- **Primary Use**: Provides the Large Language Models (LLMs) used as the "brains" for our agents.
- **Sentinel Impact**: Powers reasoning in `PolicyExpertAgent` and logistics coordination in `ResponderAgent`.
- **Note**: This is the most critical connection. Without it, the `AIProjectClient` cannot initialize conversation threads.

## 🔍 Grounding: Azure AI Search
- **Primary Use**: Vector search engine for document retrieval.
- **Sentinel Impact**: Used by `PolicyExpertAgent` to search through logistics SLAs and insurance policies for relevant disruption clauses.
- **RAG Pattern**: This resource enables **Retrieval-Augmented Generation**, ensuring agents use your actual business documents rather than just general knowledge.

## 🌐 Web Knowledge: Grounding with Bing Search
- **Primary Use**: Real-time access to the public internet.
- **Sentinel Usage**: Useful for verifying current weather data or global events that aren't yet documented in our uploaded PDF files.

## 📂 Business Data: SharePoint & Storage Accounts
- **Primary Use**: Secure ingestion of enterprise documents.
- **Sentinel Usage**: Allows the system to automatically index new files added to your company's document repositories.

## 📊 Analytics: Microsoft Fabric
- **Primary Use**: Large-scale data processing.
- **Sentinel Usage**: Optimized for scenarios requiring heavy computation of supply chain metrics before an agent generates a summary.

---

*Last Updated: April 2026*
