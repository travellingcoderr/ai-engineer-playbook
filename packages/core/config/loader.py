from pydantic_settings import BaseSettings
from pydantic import Field

class LoaderConfiguration(BaseSettings):
    strategy: str = Field(default="auto", description="How to load documents (e.g., auto, pdf, markdown)")
