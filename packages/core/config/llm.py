from pydantic_settings import BaseSettings
from pydantic import Field

class LLMConfiguration(BaseSettings):
    provider: str = Field(default="openai", description="The LLM provider (e.g., openai, gemini, anthropic)")
    model: str = Field(default="gpt-4o", description="The specific model name for the provider", alias="OPENAI_MODEL")
    openai_api_key: str | None = Field(default=None, description="OpenAI API Key", alias="OPENAI_API_KEY")
    gemini_api_key: str | None = Field(default=None, description="Google Gemini API Key")
