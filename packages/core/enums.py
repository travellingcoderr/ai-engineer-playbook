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

class AIModel(str, Enum):
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet"
    GEMINI_1_5_PRO = "gemini-1.5-pro"
