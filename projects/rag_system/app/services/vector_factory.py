from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from packages.core.enums import VectorStoreProvider

class VectorStoreFactory:
    """
    Factory class to instantiate the correct Vector Store based on configuration.
    """
    
    @staticmethod
    def create_vector_store(
        provider: VectorStoreProvider, 
        collection_name: str, 
        embeddings: Embeddings,
        **kwargs
    ) -> VectorStore:
        """
        Creates and returns a LangChain VectorStore instance.
        
        Args:
            provider: The name of the db provider ('chroma', 'qdrant')
            collection_name: The name of the collection/index
            embeddings: An instantiated Embeddings model to vectorize data
            **kwargs: Extra arguments for connection strings, etc.
        """
        # Ensure fallback to localhost if not specified
        host = kwargs.get("host", "localhost")
        port = kwargs.get("port", 8000)
        
        if provider == VectorStoreProvider.CHROMA:
            return VectorStoreFactory._create_chroma(collection_name, embeddings, host, port)
            
        elif provider == VectorStoreProvider.QDRANT:
            return VectorStoreFactory._create_qdrant(collection_name, embeddings, host, port)
            
        else:
            raise ValueError(f"Unsupported Vector Store provider: {provider}")

    @staticmethod
    def _create_chroma(collection_name: str, embeddings: Embeddings, host: str, port: int) -> VectorStore:
        try:
            from langchain_chroma import Chroma
            import chromadb
        except ImportError:
            raise ImportError("Please install chromadb and langchain-chroma to use the Chroma provider.")
            
        # Connect to a remote ChromaDB server via HTTP
        client = chromadb.HttpClient(host=host, port=port)
            
        return Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=embeddings,
        )

    @staticmethod
    def _create_qdrant(collection_name: str, embeddings: Embeddings, host: str, port: int) -> VectorStore:
        try:
            from langchain_qdrant import QdrantVectorStore
            from qdrant_client import QdrantClient
            from qdrant_client.http.models import Distance, VectorParams
        except ImportError:
            raise ImportError("Please install qdrant-client and langchain-qdrant to use the Qdrant provider.")
            
        client = QdrantClient(host=host, port=port)
        
        # Qdrant strictly requires the collection to exist before use
        if not client.collection_exists(collection_name):
            # We need to know the vector size. As a workaround during an empty init,
            # we'll generate a dummy embedding to find the correct dimension size.
            dummy_vector = embeddings.embed_query("dummy")
            vector_size = len(dummy_vector)
            
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            
        return QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embeddings,
        )
