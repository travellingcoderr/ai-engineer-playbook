# RAG System Architecture: Factory Pattern Strategy

This document outlines the architecture of the RAG (Retrieval-Augmented Generation) system. To ensure high extensibility, maintainability, and testing ease, the system relies heavily on the **Abstract Factory Pattern** for all core ML and data components.

## Why the Factory Pattern?

In the rapidly evolving AI landscape, being locked into a single provider (e.g., OpenAI, Pinecone) is risky. By abstracting our core dependencies behind factories, we achieve:
1. **Flexibility:** Swap LLMs or Vector databases by just changing an environment variable in `.env`.
2. **Cost Management:** Use cheaper open-source models for development and powerful proprietary models for production.
3. **Data Privacy:** Easily switch to local LLMs (like Ollama) and local embeddings for sensitive data without rewriting business logic.

## Core configuration

All configuration is driven by `projects/rag_system/app/core/config.py`. It reads standard environment variables and populates Pydantic models (e.g., `LLMConfiguration`, `VectorStoreConfiguration`).

```env
# Example .env configuration
LLM_PROVIDER=openai # or 'gemini', 'ollama'
EMBEDDING_PROVIDER=huggingface # or 'openai'
VECTOR_STORE_PROVIDER=chroma # or 'qdrant'
```

## The Five Factories

The overarching `rag.py` pipeline relies on five distinct factories to build the execution chain:

### 1. `LLMFactory` (`services/llm_factory.py`)
Responsible for instantiating the generation model.
- **Inputs:** `LLMConfiguration` (Provider name, Model name, API Keys).
- **Outputs:** An instantiated LLM client (e.g., `ChatOpenAI` or `ChatGoogleGenerativeAI` from LangChain).

### 2. `EmbeddingFactory` (`services/embedding_factory.py`)
Responsible for the model that converts text chunks into vector arrays.
- **Inputs:** `EmbeddingConfiguration`.
- **Outputs:** An embedding client (e.g., `OpenAIEmbeddings` or `HuggingFaceEmbeddings`).

### 3. `VectorStoreFactory` (`services/vector_factory.py`)
Responsible for the database that stores and searches the embeddings.
- **Inputs:** `VectorStoreConfiguration` AND the instantiated Embedding model (from the `EmbeddingFactory`).
- **Outputs:** A connected vector store client (e.g., ChromaDB, Qdrant).

### 4. `LoaderFactory` (`services/loader_factory.py`)
Responsible for extracting raw text from various sources.
- **Inputs:** A file path, URL, or data source identifier.
- **Outputs:** The appropriate parser (e.g., `PyPDFLoader` for `.pdf`, `UnstructuredMarkdownLoader` for `.md`).

### 5. `SplitterFactory` (`services/splitter_factory.py`)
Responsible for chunking the extracted text into semantically meaningful pieces.
- **Inputs:** `SplitterConfiguration` (Chunk size, Chunk overlap, Strategy).
- **Outputs:** A text splitter instance (e.g., `RecursiveCharacterTextSplitter`).

## Flow of Execution (`services/rag.py`)

1. Code starts in `main.py` when `/ask` is hit.
2. `main.py` calls the RAG pipeline in `services/rag.py`.
3. The RAG pipeline requests an LLM, Embedding Model, and Vector Store from their respective factories.
4. The user's query is embedded using the `EmbeddingFactory` output.
5. The `VectorStoreFactory` output is queried using the embedded query to retrieve context.
6. The retrieved context + the raw query are sent to the `LLMFactory` output to generate the final answer.
