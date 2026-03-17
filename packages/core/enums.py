from enum import Enum

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    AZURE = "azure"

class VectorStoreProvider(str, Enum):
    CHROMA = "chroma"
    QDRANT = "qdrant"
    PINECONE = "pinecone"

class EmbeddingProvider(str, Enum):
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    COHERE = "cohere"

class GatewayMode(str, Enum):
    SIMULATION = "simulation"
    PRODUCTION = "production"

class RoutingStrategy(str, Enum):
    PRIORITY = "priority"
    ROUND_ROBIN = "round_robin"
    RANDOM = "random"
    WEIGHTED = "weighted"
