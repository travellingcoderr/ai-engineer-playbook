from typing import List, Optional, Dict, Any
from packages.core.services import LLMFactory
from packages.core.enums import AIModel, EmbeddingModel
from langchain_core.documents import Document
from langchain_postgres import PGVector
import os

class RAGService:
    """
    Centralized RAG service in packages/core to be reused by all projects.
    """
    def __init__(self, connection_string: str, collection_name: str = "knowledge"):
        self.connection_string = connection_string
        self.collection_name = collection_name
        self.embeddings = self._get_embeddings()
        self.vector_store = self._get_vector_store()

    def _get_embeddings(self):
        return LLMFactory.create_embeddings(
            model_name="text-embedding-3-small",
            instrument=True,
            component="rag_service",
            operation="embedding_generation",
        )

    def _get_vector_store(self):
        from packages.core.services.vector_factory import VectorStoreFactory
        return VectorStoreFactory.create_vector_store(
            embeddings=self.embeddings,
            collection_name=self.collection_name,
            connection=self.connection_string
        )

    def add_documents(self, documents: List[Document]):
        self.vector_store.add_documents(documents)

    def search(self, query: str, k: int = 4) -> List[Document]:
        return self.vector_store.similarity_search(query, k=k)

    def search_with_score(self, query: str, k: int = 4) -> List[tuple[Document, float]]:
        return self.vector_store.similarity_search_with_score(query, k=k)
