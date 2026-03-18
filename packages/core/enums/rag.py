from enum import Enum

class VectorStoreProvider(str, Enum):
    CHROMA = "chroma"
    QDRANT = "qdrant"
    PINECONE = "pinecone"
    PGVECTOR = "pgvector"

class EmbeddingProvider(str, Enum):
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    COHERE = "cohere"

class EmbeddingModel(str, Enum):
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"

class LoaderStrategy(str, Enum):
    AUTO = "auto"
    SIMPLE = "simple"
    PDF = "pdf"
    MARKDOWN = "markdown"
    TEXT = "text"
    WEB = "web"
    DIRECTORY = "directory"

class SplitterStrategy(str, Enum):
    CHARACTER = "character"
    RECURSIVE = "recursive"
    MARKDOWN = "markdown"
    PYTHON = "python"
