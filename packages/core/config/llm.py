from pydantic import Field, BaseModel

class LLMConfiguration(BaseModel):
    provider: str = Field(default="openai", description="The LLM provider (e.g., openai, gemini, anthropic)", alias="LLM_PROVIDER")
    model: str = Field(default="gpt-4o", description="The specific model name for the provider", alias="OPENAI_MODEL")
    openai_api_key: str | None = Field(default=None, description="OpenAI API Key", alias="OPENAI_API_KEY")
    openai_api_base: str | None = Field(default=None, description="OpenAI-compatible API base URL", alias="OPENAI_API_BASE")
    gemini_api_key: str | None = Field(default=None, description="Google Gemini API Key")
