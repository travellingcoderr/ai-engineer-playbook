from pydantic import Field, BaseModel
from packages.core.enums import LLMProvider, AIModel

class LLMConfiguration(BaseModel):
    provider: LLMProvider = Field(default=LLMProvider.OPENAI, description="The LLM provider (e.g., openai, gemini, anthropic)", alias="LLM_PROVIDER")
    model: AIModel = Field(default=AIModel.GPT_4O, description="The specific model name for the provider", alias="OPENAI_MODEL")
    openai_api_key: str | None = Field(default=None, description="OpenAI API Key", alias="OPENAI_API_KEY")
    openai_api_base: str | None = Field(default=None, description="OpenAI-compatible API base URL", alias="OPENAI_API_BASE")
    gemini_api_key: str | None = Field(default=None, description="Google Gemini API Key")
