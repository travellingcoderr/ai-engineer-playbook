# RAG System API Services

This document outlines all the available HTTP endpoints exposed by the FastAPI application in this project.

## 1. POST `/ingest`
- **Description:** Ingests a new document into the Artificial Intelligence Vector Database to be used as retrieved context for the Large Language Model.
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `file` (UploadFile): The physical file (PDF, Markdown, etc.) you wish to upload.
- **Response:**
  - `status`: String ("success")
  - `chunks_ingested`: Integer (Number of text blocks the document was split into)
  - `file`: String (The original filename)

## 2. GET `/ask`
- **Description:** Queries the AI using the Retrieval-Augmented Generation (RAG) pipeline. The system will search the vector database for the top 3 most relevant context chunks and instruct the LLM to answer the question using only that context.
- **Parameters:**
  - `q` (String, required): The question to ask the AI.
- **Response:**
  - `answer`: String (The generated answer from the LLM)

---

>**Note:** FastAPI automatically provides interactive Swagger documentation for all these routes natively at `http://localhost:8000/docs` while the application is running.
